from __future__ import annotations
import attr


@attr.s(frozen=True, slots=True)
class PullRequest:
    title: str = attr.ib()
    state: str = attr.ib()
    number: int = attr.ib()
    head_ref: str = attr.ib()  # branch where the changes are
    base_ref: str = attr.ib()  # branch where we want to merge the changes into
    merged: bool = attr.ib()
    url: str = attr.ib()
    html_url: str = attr.ib()

    @classmethod
    def from_github_pull_request(cls, pull_request):
        return cls(
            pull_request.title,
            pull_request.state,
            pull_request.number,
            pull_request.head.ref,
            pull_request.base.ref,
            pull_request.merged,
            pull_request.url,
            pull_request.html_url,
        )


@attr.s(frozen=True, slots=True)
class PullRequests:
    pulls = attr.ib()
    pulls_dict = attr.ib()

    def filter(self, state) -> PullRequests:
        return PullRequests(
            {k: v for k, v in self.pulls_dict.items() if v.state == state}
        )

    def __getitem__(self, number: str) -> PullRequest:
        return self.pulls_dict[number]

    def __contains__(self, number: int) -> bool:
        return number in self.pulls_dict

    @classmethod
    def from_github_api(cls):
        return cls()

    def __iter__(self):
        return iter(self.pulls)

    @classmethod
    def from_github_get_pulls(cls, pull_requests):
        pulls_list = []
        pulls_dict = {}
        page_index = 0
        pulls_in_page = [PullRequest.from_github_pull_request(x) for x in pull_requests.get_page(page_index)]
        while pulls_in_page:
            pulls_list.extend(pulls_in_page)
            pulls_dict.update({
                pull.number: pull for pull in pulls_in_page
            })
            page_index += 1
            pulls_in_page = pull_requests.get_page(page_index)
        return cls(pulls_list, pulls_dict)
