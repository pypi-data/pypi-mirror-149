from git import Repo, Remote


class GitService(object):
    """
    A class for interacting with a local Git project
    """

    repository: Repo
    remote: Remote

    def __init__(self, local_repository_path: str, branch_name: str = None) -> None:
        """Initialise the Git client
        """
        # TODO: branch name
        self.repository = Repo(local_repository_path)
        self.branch = self.repository.active_branch
        self.remote = self.repository.remote('origin')

        if not self.__is_valid_git_project():
            raise Exception('Not a valid git project')

        return

    def __is_valid_git_project(self) -> bool:
        """Check if the supplied repository is valid
        """
        try:
            assert not self.repository.bare
        except Exception:
            return False

        return True

    def add_folder_to_staging(self, relative_folder_path: str) -> None:
        """Add the folder and all its contents to the git staging area

        Parameters
        ----------
          relative_folder_path: str
            represents the relative path to the folder from the root of
            the git directory
        """
        self.repository.index.add([relative_folder_path])
        return

    def delete_folder_from_staging(self, relative_folder_path: str) -> None:
        self.repository.index.remove([relative_folder_path], False, r=True, ignore_unmatch=True)
        return

    def commit(self, commit_message: str) -> str:
        """Create a new commit on the current branch

        Parameters
        ----------
          commit_message: str
            representing the commit message
        """
        self.repository.index.commit(commit_message)
        return self.repository.head.commit.hexsha

    def pull(self) -> None:
        """Pull from the default remote repository
        """
        self.remote.pull(self.branch, ff_only=True)
        return

    def push(self) -> None:
        """Push to the default remote repository
        """
        self.remote.push()
        return

    def get_remote_url(self) -> str:
        return self.remote.url

    def get_current_branch_name(self) -> str:
        return self.repository.active_branch.name
