import datetime
import logging
import os
import shutil
import subprocess
import tempfile
import time
from typing import Optional


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


EFS_WORKSPACE_DIR = os.environ.get("EFS_WORKSPACE_DIR", "/efs/workspaces")
EFS_OBJECTS_DIR = os.environ.get("EFS_OBJECTS_DIR", "/efs/workspaces/shared_objects")
EFS_CREDS_DIR = os.environ.get("EFS_CREDS_DIR", "/efs/generated_credentials")


def optimize_git_repo(directory: str, shared_repo: str) -> None:
    """Optimize the space usage of a git repo by syncing objects to a shared repo.

    Any objects in the source repo will be replicated to the shared repo, and then
    deleted from the source repo. The source repo is setup to reference objects in
    the shared repo via the `.git/objects/info/alternates` mechanism.

    Args:
        directory: The directory to optimize.
        shared_repo: The path that should be used to hold shared objects. This path
            will be created if it doesn't already exist. Multiple checkouts of the
            same repo can share the objects stored in the shared repo.
    """
    start = time.time()
    objects_path = "{}/.git/objects".format(directory)
    if os.path.exists(objects_path):
        if not os.path.exists(shared_repo):
            os.makedirs(os.path.dirname(shared_repo), exist_ok=True)
            # TODO(ekl) it's faster to do a copy of just the objects dir, but it seems
            # we need to git clone in order for alternates to be recognized as valid.
            subprocess.check_call(  # noqa
                "git clone --bare {}/ {}/".format(directory, shared_repo), shell=True,
            )
        shared_objects_dir = os.path.join(shared_repo, "objects")
        subprocess.check_call(  # noqa
            "rsync -a {}/ {}/".format(objects_path, shared_objects_dir), shell=True
        )
        subprocess.check_call("rm -rf {}".format(objects_path), shell=True)  # noqa
        os.makedirs(os.path.join(objects_path, "info"), exist_ok=True)
        with open(os.path.join(objects_path, "info/alternates"), "w") as f:
            f.write("{}\n".format(shared_objects_dir))
    logger.info(
        "Synced git objects for {} to {} in {}s.".format(
            directory, shared_repo, time.time() - start
        )
    )


def create_snapshot_zip(directory: str, auto: bool) -> str:
    """Create a snapshot of the given directory.

    The snapshot will include all git tracked files as well as unstaged
    (but otherwise trackable) files. It will also include the full
    contents of the `.git` folder. To optimize the disk space usage of
    snapshots, call `optimize_git_repo` on the repo directory prior to
    calling `create_snapshot_zip`.

    Args:
        directory: Path of the directory to snapshot.

    Returns:
        Path of a .zip file that contains the snapshot files.
    """

    start = time.time()
    orig = os.path.abspath(os.curdir)
    prefix = "snapshot_{}_".format(datetime.datetime.now().isoformat())
    if auto:
        prefix += "auto_"
    target = tempfile.mktemp(suffix=".zip", prefix=prefix)
    try:
        os.chdir(directory)
        subprocess.check_call(  # noqa
            "(git ls-files -co --exclude-standard || true; find .git || true) | "
            f"zip --symlinks -@ -0 -q {target}",
            shell=True,
        )
    finally:
        os.chdir(orig)

    assert os.path.exists(target), target
    logger.info(
        "Created snapshot for {} at {} of size {} in {}s.".format(
            directory, target, os.path.getsize(target), time.time() - start
        )
    )
    return target


def unpack_snapshot_zip(zip_path: str, directory: str) -> None:
    """Unpack a snapshot to the given directory.

    Args:
        zip_path: Path of the zip returned by create_snapshot_zip.
        directory: Output directory to unpack the zip into.
    """

    start = time.time()
    os.makedirs(directory, exist_ok=True)
    subprocess.check_call(  # noqa
        "unzip -X -o -q {} -d {}".format(zip_path, directory), shell=True
    )
    logger.info(
        "Unpacked snapshot {} to {} in {}s.".format(
            zip_path, directory, time.time() - start
        )
    )


def compute_content_hash(zip_path: str) -> bytes:
    """Return the md5 hash of a given zipfile on disk."""
    md5 = subprocess.check_output(  # noqa
        "unzip -p {} | md5sum -b | cut -f1 -d ' '".format(zip_path), shell=True
    )
    md5 = md5.strip()
    return md5


def get_or_create_snapshot_zip(directory: str, auto: bool) -> str:
    """Create a snapshot zip, or return the last snapshot if unchanged.

    A corresponding .md5 file is created alongside the snapshot zip.
    """
    new_zip = create_snapshot_zip(directory, auto)
    new_hash = compute_content_hash(new_zip)
    old_zip = find_latest()
    if old_zip:
        try:
            old_hash: Optional[bytes] = open(old_zip + ".md5", "rb").read().strip()
        except Exception:
            logger.warning("Failed to read md5 file")
            old_hash = None
    else:
        old_hash = None
    logger.info("Content hashes {!r} vs {!r}".format(old_hash, new_hash))
    if old_hash == new_hash:
        logger.info("Content hash unchanged, not saving new snapshot.")
        os.unlink(new_zip)
        assert old_zip is not None
        return old_zip
    else:
        with open(new_zip + ".md5", "wb") as f:
            f.write(new_hash)
        return new_zip


def do_snapshot(auto: bool = False):
    """Command to create a snapshot within an Anyscale workspace.

    Can be run via `python -m anyscale.snapshot_util snapshot`.
    """
    home = os.environ["ANYSCALE_WORKING_DIR"]
    workspace_dir = os.path.join(
        EFS_WORKSPACE_DIR, os.environ["ANYSCALE_EXPERIMENTAL_WORKSPACE_ID"]
    )
    snapshot_dir = os.path.join(workspace_dir, "snapshots")
    # TODO(ekl) should we isolate the objects by workspace or repo?
    optimize_git_repo(home, EFS_OBJECTS_DIR)
    zip = get_or_create_snapshot_zip(home, auto)

    # If the zip was already on EFS, we're done.
    if zip.startswith(snapshot_dir):
        return

    # Otherwise, move the zip into EFS along with its md5 file.
    os.makedirs(snapshot_dir, exist_ok=True)
    shutil.move(zip, os.path.join(snapshot_dir, os.path.basename(zip)))
    shutil.move(
        zip + ".md5", os.path.join(snapshot_dir, os.path.basename(zip) + ".md5")
    )
    shutil.copy(
        os.path.expanduser("~/.bash_history"),
        os.path.join(workspace_dir, ".bash_history"),
    )


def find_latest() -> Optional[str]:
    """Return path to latest .zip snapshot, if it exists."""
    workspace_dir = os.path.join(
        EFS_WORKSPACE_DIR, os.environ["ANYSCALE_EXPERIMENTAL_WORKSPACE_ID"]
    )
    snapshot_dir = os.path.join(workspace_dir, "snapshots")
    if not os.path.exists(snapshot_dir):
        return None
    snapshots = sorted([x for x in os.listdir(snapshot_dir) if x.endswith(".zip")])
    if not snapshots:
        return None
    return os.path.join(snapshot_dir, snapshots[-1])


def restore_latest():
    """Command to restore the latest snapshot within an Anyscale workspace.

    Can be run via `python -m anyscale.snapshot_util restore`.
    """
    latest = find_latest()
    if not latest:
        return
    home = os.environ["ANYSCALE_WORKING_DIR"]
    workspace_dir = os.path.join(
        EFS_WORKSPACE_DIR, os.environ["ANYSCALE_EXPERIMENTAL_WORKSPACE_ID"]
    )
    unpack_snapshot_zip(latest, home)
    shutil.copy(
        os.path.join(workspace_dir, ".bash_history"),
        os.path.expanduser("~/.bash_history"),
    )


def env_hook(runtime_env):
    """Env hook for including the working dir in the runtime_env by default.

    This should be set as `RAY_RUNTIME_ENV_HOOK=anyscale.snapshot_util.env_hook`.
    """
    if not runtime_env:
        runtime_env = {}
    if not runtime_env.get("working_dir"):
        runtime_env["working_dir"] = os.environ["ANYSCALE_WORKING_DIR"]
    if not runtime_env["working_dir"].endswith(".zip"):
        workspace = runtime_env["working_dir"]
        optimize_git_repo(workspace, EFS_OBJECTS_DIR)
        zipfile = get_or_create_snapshot_zip(workspace, auto=False)
        runtime_env["working_dir"] = zipfile
    print("Updated runtime env to {}".format(runtime_env))
    return runtime_env


def setup_credentials():
    """Command to create SSH credentials for the workspace.

    We generate unique Anyscale SSH keys for each username. This call will inject
    the key for the current user into the workspace.
    """
    username = os.environ.get("ANYSCALE_EXPERIMENTAL_USERNAME", "unknown_user")
    private_key = os.path.join(EFS_CREDS_DIR, username, "id_rsa")
    public_key = os.path.join(EFS_CREDS_DIR, username, "id_rsa.pub")
    os.makedirs("/home/ray/.ssh", exist_ok=True)
    if os.path.exists(private_key):
        # Copy down from EFS.
        shutil.copy(private_key, "/home/ray/.ssh/id_rsa")
        shutil.copy(public_key, "/home/ray/.ssh/id_rsa.pub")
    else:
        # Copy up to EFS.
        subprocess.check_call(  # noqa
            "echo y | ssh-keygen -t rsa -f /home/ray/.ssh/id_rsa -N ''", shell=True
        )
        os.makedirs(os.path.dirname(private_key), exist_ok=True)
        shutil.copy("/home/ray/.ssh/id_rsa", private_key)
        shutil.copy("/home/ray/.ssh/id_rsa.pub", public_key)


def autosnapshot_loop():
    interval = int(os.environ.get("ANYSCALE_SNAPSHOT_INTERVAL", 300))
    logger.info("Started autosnapshot loop with interval {}".format(interval))
    while True:
        time.sleep(interval)
        do_snapshot(auto=True)


if __name__ == "__main__":
    import sys

    if sys.argv[1] == "snapshot":
        do_snapshot()
    elif sys.argv[1] == "autosnapshot":
        autosnapshot_loop()
    elif sys.argv[1] == "restore":
        restore_latest()
    elif sys.argv[1] == "setup_credentials":
        setup_credentials()
    else:
        print("unknown arg")
