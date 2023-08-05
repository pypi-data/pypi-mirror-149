from swh.graphql import server


class Archive:
    def __init__(self):
        self.storage = server.get_storage()

    def get_origin(self, url):
        return self.storage.origin_get([url])[0]

    def get_origins(self, after=None, first=50, url_pattern=None):
        # STORAGE-TODO
        # Make them a single function in the backend
        if url_pattern is None:
            return self.storage.origin_list(page_token=after, limit=first)

        return self.storage.origin_search(
            url_pattern=url_pattern, page_token=after, limit=first
        )

    def get_origin_visits(self, origin_url, after=None, first=50):
        return self.storage.origin_visit_get(origin_url, page_token=after, limit=first)

    def get_origin_visit(self, origin_url, visit_id):
        return self.storage.origin_visit_get_by(origin_url, visit_id)

    def get_origin_latest_visit(self, origin_url):
        return self.storage.origin_visit_get_latest(origin_url)

    def get_visit_status(self, origin_url, visit_id, after=None, first=50):
        return self.storage.origin_visit_status_get(
            origin_url, visit_id, page_token=after, limit=first
        )

    def get_latest_visit_status(self, origin_url, visit_id):
        return self.storage.origin_visit_status_get_latest(origin_url, visit_id)

    def get_origin_snapshots(self, origin_url):
        return self.storage.origin_snapshot_get_all(origin_url)

    def is_snapshot_available(self, snapshot_ids):
        return not self.storage.snapshot_missing(snapshot_ids)

    def get_snapshot_branches(self, snapshot, after, first, target_types, name_include):
        return self.storage.snapshot_get_branches(
            snapshot,
            branches_from=after,
            branches_count=first,
            target_types=target_types,
            branch_name_include_substring=name_include,
        )

    def get_revisions(self, revision_ids):
        return self.storage.revision_get(revision_ids=revision_ids)

    def get_revision_log(self, revision_ids, after=None, first=50):
        return self.storage.revision_log(revisions=revision_ids, limit=first)

    def get_releases(self, release_ids):
        return self.storage.release_get(releases=release_ids)

    def is_directory_available(self, directory_ids):
        return not self.storage.directory_missing(directory_ids)

    def get_directory_entries(self, directory_id, after=None, first=50):
        return self.storage.directory_get_entries(
            directory_id, limit=first, page_token=after
        )

    def get_content(self, content_id):
        # FIXME, only for tests
        return self.storage.content_find({"sha1_git": content_id})
