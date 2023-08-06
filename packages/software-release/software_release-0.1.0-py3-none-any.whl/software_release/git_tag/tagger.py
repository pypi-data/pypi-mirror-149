from .tagger_interface import TaggerInterface


class GitTagger(TaggerInterface):

    def tag_commit(self, repository, tag, reference=None, **kwargs):
        message = kwargs.pop('message', None)
        tag_reference = repository.repo_proxy.create_tag(
            tag,
            ref={None: 'HEAD'}.get(reference, reference),
            message=message,
            force=False,
            **kwargs
        )
        return tag_reference
