"""Declare Mediawiki database table Mapping."""

from __future__ import annotations

from datetime import datetime  # noqa: TC003
from decimal import Decimal  # noqa: TC003
from types import MappingProxyType

from sqlalchemy import Dialect, LargeBinary, TypeDecorator
from sqlalchemy.orm import DeclarativeBase, Mapped as Col, mapped_column as col

__all__ = (
    "Actor",
    "Archive",
    "Block",
    "BlockTarget",
    "BotPasswords",
    "Category",
    "Categorylinks",
    "ChangeTag",
    "ChangeTagDef",
    "Comment",
    "Content",
    "ContentModels",
    "Externallinks",
    "Filearchive",
    "Image",
    "Imagelinks",
    "Interwiki",
    "IpChanges",
    "Ipblocks",
    "IpblocksRestrictions",
    "Iwlinks",
    "Job",
    "L10nCache",
    "Langlinks",
    "Linktarget",
    "LogSearch",
    "Logging",
    "ModuleDeps",
    "Objectcache",
    "Oldimage",
    "Page",
    "PageAssessments",
    "PageAssessmentsProjects",
    "PageProps",
    "PageRestrictions",
    "Pagelinks",
    "ProtectedTitles",
    "Querycache",
    "QuerycacheInfo",
    "Querycachetwo",
    "Recentchanges",
    "Redirect",
    "Revision",
    "Searchindex",
    "SiteIdentifiers",
    "SiteStats",
    "Sites",
    "SlotRoles",
    "Slots",
    "Templatelinks",
    "Text",
    "Updatelog",
    "Uploadstash",
    "User",
    "UserAutocreateSerial",
    "UserFormerGroups",
    "UserGroups",
    "UserNewtalk",
    "UserProperties",
    "Watchlist",
    "WatchlistExpiry",
    "WbChanges",
    "WbChangesSubscription",
    "WbIdCounters",
    "WbItemsPerSite",
    "WbPropertyInfo",
    "WbtItemTerms",
    "WbtPropertyTerms",
    "WbtTermInLang",
    "WbtText",
    "WbtTextInLang",
    "WbtType",
)


class Base(DeclarativeBase):
    """The Base class of ORM definitions."""


class BinaryDecoder(TypeDecorator):
    """An SQLAlchemy type decorator for processing text-type values.

    It encodes str to bytes on the way in and decodes bytes to str on
    the way out.
    """

    impl = LargeBinary

    cache_ok = True

    _encoding_config = MappingProxyType({
        "encoding": "utf-8",
        "errors": "backslashreplace",
    })

    def process_bind_param(
        self,
        value: str | None,
        dialect: Dialect,  # noqa: ARG002
    ) -> bytes | None:
        """Preprocess str values before executing a query.

        Args:
            value: The string value to encode.
            dialect: The database dialect.

        Returns:
            The encoded binary value or None if the input value is None.
        """
        if value is None:
            return None
        return value.encode(**self._encoding_config)

    def process_result_value(
        self,
        value: bytes | None,
        dialect: Dialect,  # noqa: ARG002
    ) -> str | None:
        """Process bytes values obtained from a query.

        Args:
            value: The binary value to decode.
            dialect: The database dialect.

        Returns:
            The decoded string value or None if the input value is None.
        """
        if value is None:
            return None
        return value.decode(**self._encoding_config)


class Actor(Base):
    """The table ``actor``.

    Attributes:
        actor_id: ``int``
        actor_user: ``int``
        actor_name: ``str``
    """

    __tablename__ = "actor"
    actor_id: Col[int] = col(primary_key=True)
    actor_user: Col[int] = col()
    actor_name: Col[str] = col(BinaryDecoder)


class Archive(Base):
    """The table ``archive``.

    Attributes:
        ar_id: ``int``
        ar_namespace: ``int``
        ar_title: ``str``
        ar_comment_id: ``int``
        ar_actor: ``Decimal``
        ar_timestamp: ``str``
        ar_minor_edit: ``int``
        ar_rev_id: ``int``
        ar_deleted: ``int``
        ar_len: ``int``
        ar_page_id: ``int``
        ar_parent_id: ``int``
        ar_sha1: ``str``
    """

    __tablename__ = "archive"
    ar_id: Col[int] = col(primary_key=True)
    ar_namespace: Col[int] = col()
    ar_title: Col[str] = col(BinaryDecoder)
    ar_comment_id: Col[int] = col()
    ar_actor: Col[Decimal] = col()
    ar_timestamp: Col[str] = col(BinaryDecoder)
    ar_minor_edit: Col[int] = col()
    ar_rev_id: Col[int] = col()
    ar_deleted: Col[int] = col()
    ar_len: Col[int] = col()
    ar_page_id: Col[int] = col()
    ar_parent_id: Col[int] = col()
    ar_sha1: Col[str] = col(BinaryDecoder)


class Block(Base):
    """The table ``block``.

    Attributes:
        bl_id: ``int``
        bl_target: ``int``
        bl_by_actor: ``int``
        bl_reason_id: ``int``
        bl_timestamp: ``str``
        bl_anon_only: ``int``
        bl_create_account: ``int``
        bl_enable_autoblock: ``int``
        bl_expiry: ``str``
        bl_deleted: ``int``
        bl_block_email: ``int``
        bl_allow_usertalk: ``int``
        bl_parent_block_id: ``int``
        bl_sitewide: ``int``
    """

    __tablename__ = "block"
    bl_id: Col[int] = col(primary_key=True)
    bl_target: Col[int] = col()
    bl_by_actor: Col[int] = col()
    bl_reason_id: Col[int] = col()
    bl_timestamp: Col[str] = col(BinaryDecoder)
    bl_anon_only: Col[int] = col()
    bl_create_account: Col[int] = col()
    bl_enable_autoblock: Col[int] = col()
    bl_expiry: Col[str] = col(BinaryDecoder)
    bl_deleted: Col[int] = col()
    bl_block_email: Col[int] = col()
    bl_allow_usertalk: Col[int] = col()
    bl_parent_block_id: Col[int] = col()
    bl_sitewide: Col[int] = col()


class BlockTarget(Base):
    """The table ``block_target``.

    Attributes:
        bt_id: ``int``
        bt_address: ``str``
        bt_user: ``int``
        bt_user_text: ``str``
        bt_auto: ``int``
        bt_range_start: ``str``
        bt_range_end: ``str``
        bt_ip_hex: ``str``
        bt_count: ``int``
    """

    __tablename__ = "block_target"
    bt_id: Col[int] = col(primary_key=True)
    bt_address: Col[str] = col(BinaryDecoder)
    bt_user: Col[int] = col()
    bt_user_text: Col[str] = col(BinaryDecoder)
    bt_auto: Col[int] = col()
    bt_range_start: Col[str] = col(BinaryDecoder)
    bt_range_end: Col[str] = col(BinaryDecoder)
    bt_ip_hex: Col[str] = col(BinaryDecoder)
    bt_count: Col[int] = col()


class BotPasswords(Base):
    """The table ``bot_passwords``.

    Attributes:
        bp_user: ``int``
        bp_app_id: ``str``
        bp_password: ``str``
        bp_token: ``str``
        bp_restrictions: ``str``
        bp_grants: ``str``
    """

    __tablename__ = "bot_passwords"
    bp_user: Col[int] = col(primary_key=True)
    bp_app_id: Col[str] = col(BinaryDecoder, primary_key=True)
    bp_password: Col[str] = col(BinaryDecoder)
    bp_token: Col[str] = col(BinaryDecoder)
    bp_restrictions: Col[str] = col(BinaryDecoder)
    bp_grants: Col[str] = col(BinaryDecoder)


class Category(Base):
    """The table ``category``.

    Attributes:
        cat_id: ``int``
        cat_title: ``str``
        cat_pages: ``int``
        cat_subcats: ``int``
        cat_files: ``int``
    """

    __tablename__ = "category"
    cat_id: Col[int] = col(primary_key=True)
    cat_title: Col[str] = col(BinaryDecoder)
    cat_pages: Col[int] = col()
    cat_subcats: Col[int] = col()
    cat_files: Col[int] = col()


class Categorylinks(Base):
    """The table ``categorylinks``.

    Attributes:
        cl_from: ``int``
        cl_to: ``str``
        cl_sortkey: ``str``
        cl_sortkey_prefix: ``str``
        cl_timestamp: ``datetime``
        cl_collation: ``str``
        cl_type: ``str``
    """

    __tablename__ = "categorylinks"
    cl_from: Col[int] = col(primary_key=True)
    cl_to: Col[str] = col(BinaryDecoder, primary_key=True)
    cl_sortkey: Col[str] = col(BinaryDecoder)
    cl_sortkey_prefix: Col[str] = col(BinaryDecoder)
    cl_timestamp: Col[datetime] = col()
    cl_collation: Col[str] = col(BinaryDecoder)
    cl_type: Col[str] = col(BinaryDecoder)


class ChangeTag(Base):
    """The table ``change_tag``.

    Attributes:
        ct_id: ``int``
        ct_rc_id: ``int``
        ct_log_id: ``int``
        ct_rev_id: ``int``
        ct_params: ``str``
        ct_tag_id: ``int``
    """

    __tablename__ = "change_tag"
    ct_id: Col[int] = col(primary_key=True)
    ct_rc_id: Col[int] = col()
    ct_log_id: Col[int] = col()
    ct_rev_id: Col[int] = col()
    ct_params: Col[str] = col(BinaryDecoder)
    ct_tag_id: Col[int] = col()


class ChangeTagDef(Base):
    """The table ``change_tag_def``.

    Attributes:
        ctd_id: ``int``
        ctd_name: ``str``
        ctd_user_defined: ``int``
        ctd_count: ``int``
    """

    __tablename__ = "change_tag_def"
    ctd_id: Col[int] = col(primary_key=True)
    ctd_name: Col[str] = col(BinaryDecoder)
    ctd_user_defined: Col[int] = col()
    ctd_count: Col[int] = col()


class Comment(Base):
    """The table ``comment``.

    Attributes:
        comment_id: ``int``
        comment_hash: ``int``
        comment_text: ``str``
        comment_data: ``str``
    """

    __tablename__ = "comment"
    comment_id: Col[int] = col(primary_key=True)
    comment_hash: Col[int] = col()
    comment_text: Col[str] = col(BinaryDecoder)
    comment_data: Col[str] = col(BinaryDecoder)


class Content(Base):
    """The table ``content``.

    Attributes:
        content_id: ``int``
        content_size: ``int``
        content_sha1: ``str``
        content_model: ``int``
        content_address: ``str``
    """

    __tablename__ = "content"
    content_id: Col[int] = col(primary_key=True)
    content_size: Col[int] = col()
    content_sha1: Col[str] = col(BinaryDecoder)
    content_model: Col[int] = col()
    content_address: Col[str] = col(BinaryDecoder)


class ContentModels(Base):
    """The table ``content_models``.

    Attributes:
        model_id: ``int``
        model_name: ``str``
    """

    __tablename__ = "content_models"
    model_id: Col[int] = col(primary_key=True)
    model_name: Col[str] = col(BinaryDecoder)


class Externallinks(Base):
    """The table ``externallinks``.

    Attributes:
        el_id: ``int``
        el_from: ``int``
        el_to_domain_index: ``str``
        el_to_path: ``str``
    """

    __tablename__ = "externallinks"
    el_id: Col[int] = col(primary_key=True)
    el_from: Col[int] = col()
    el_to_domain_index: Col[str] = col(BinaryDecoder)
    el_to_path: Col[str] = col(BinaryDecoder)


class Filearchive(Base):
    """The table ``filearchive``.

    Attributes:
        fa_id: ``int``
        fa_name: ``str``
        fa_archive_name: ``str``
        fa_storage_group: ``str``
        fa_storage_key: ``str``
        fa_deleted_user: ``int``
        fa_deleted_timestamp: ``str``
        fa_deleted_reason_id: ``int``
        fa_size: ``int``
        fa_width: ``int``
        fa_height: ``int``
        fa_metadata: ``str``
        fa_bits: ``int``
        fa_media_type: ``str``
        fa_major_mime: ``str``
        fa_minor_mime: ``str``
        fa_description_id: ``Decimal``
        fa_actor: ``int``
        fa_timestamp: ``str``
        fa_deleted: ``int``
        fa_sha1: ``str``
    """

    __tablename__ = "filearchive"
    fa_id: Col[int] = col(primary_key=True)
    fa_name: Col[str] = col(BinaryDecoder)
    fa_archive_name: Col[str] = col(BinaryDecoder)
    fa_storage_group: Col[str] = col(BinaryDecoder)
    fa_storage_key: Col[str] = col(BinaryDecoder)
    fa_deleted_user: Col[int] = col()
    fa_deleted_timestamp: Col[str] = col(BinaryDecoder)
    fa_deleted_reason_id: Col[int] = col()
    fa_size: Col[int] = col()
    fa_width: Col[int] = col()
    fa_height: Col[int] = col()
    fa_metadata: Col[str] = col(BinaryDecoder)
    fa_bits: Col[int] = col()
    fa_media_type: Col[str] = col(BinaryDecoder)
    fa_major_mime: Col[str] = col(BinaryDecoder)
    fa_minor_mime: Col[str] = col(BinaryDecoder)
    fa_description_id: Col[Decimal] = col()
    fa_actor: Col[int] = col()
    fa_timestamp: Col[str] = col(BinaryDecoder)
    fa_deleted: Col[int] = col()
    fa_sha1: Col[str] = col(BinaryDecoder)


class Image(Base):
    """The table ``image``.

    Attributes:
        img_name: ``str``
        img_size: ``int``
        img_width: ``int``
        img_height: ``int``
        img_metadata: ``str``
        img_bits: ``int``
        img_media_type: ``str``
        img_major_mime: ``str``
        img_minor_mime: ``str``
        img_description_id: ``Decimal``
        img_actor: ``int``
        img_timestamp: ``str``
        img_sha1: ``str``
    """

    __tablename__ = "image"
    img_name: Col[str] = col(BinaryDecoder, primary_key=True)
    img_size: Col[int] = col()
    img_width: Col[int] = col()
    img_height: Col[int] = col()
    img_metadata: Col[str] = col(BinaryDecoder)
    img_bits: Col[int] = col()
    img_media_type: Col[str] = col(BinaryDecoder)
    img_major_mime: Col[str] = col(BinaryDecoder)
    img_minor_mime: Col[str] = col(BinaryDecoder)
    img_description_id: Col[Decimal] = col()
    img_actor: Col[int] = col()
    img_timestamp: Col[str] = col(BinaryDecoder)
    img_sha1: Col[str] = col(BinaryDecoder)


class Imagelinks(Base):
    """The table ``imagelinks``.

    Attributes:
        il_from: ``int``
        il_from_namespace: ``int``
        il_to: ``str``
    """

    __tablename__ = "imagelinks"
    il_from: Col[int] = col(primary_key=True)
    il_from_namespace: Col[int] = col()
    il_to: Col[str] = col(BinaryDecoder, primary_key=True)


class Interwiki(Base):
    """The table ``interwiki``.

    Attributes:
        iw_prefix: ``str``
        iw_url: ``str``
        iw_api: ``str``
        iw_wikiid: ``str``
        iw_local: ``int``
        iw_trans: ``int``
    """

    __tablename__ = "interwiki"
    iw_prefix: Col[str] = col(BinaryDecoder, primary_key=True)
    iw_url: Col[str] = col(BinaryDecoder)
    iw_api: Col[str] = col(BinaryDecoder)
    iw_wikiid: Col[str] = col(BinaryDecoder)
    iw_local: Col[int] = col()
    iw_trans: Col[int] = col()


class IpChanges(Base):
    """The table ``ip_changes``.

    Attributes:
        ipc_rev_id: ``int``
        ipc_rev_timestamp: ``str``
        ipc_hex: ``str``
    """

    __tablename__ = "ip_changes"
    ipc_rev_id: Col[int] = col(primary_key=True)
    ipc_rev_timestamp: Col[str] = col(BinaryDecoder)
    ipc_hex: Col[str] = col(BinaryDecoder)


class Ipblocks(Base):
    """The table ``ipblocks``.

    Attributes:
        ipb_id: ``int``
        ipb_address: ``str``
        ipb_user: ``int``
        ipb_by_actor: ``int``
        ipb_reason_id: ``int``
        ipb_timestamp: ``str``
        ipb_auto: ``int``
        ipb_anon_only: ``int``
        ipb_create_account: ``int``
        ipb_enable_autoblock: ``int``
        ipb_expiry: ``str``
        ipb_range_start: ``str``
        ipb_range_end: ``str``
        ipb_deleted: ``int``
        ipb_block_email: ``int``
        ipb_allow_usertalk: ``int``
        ipb_parent_block_id: ``int``
        ipb_sitewide: ``int``
    """

    __tablename__ = "ipblocks"
    ipb_id: Col[int] = col(primary_key=True)
    ipb_address: Col[str] = col(BinaryDecoder)
    ipb_user: Col[int] = col()
    ipb_by_actor: Col[int] = col()
    ipb_reason_id: Col[int] = col()
    ipb_timestamp: Col[str] = col(BinaryDecoder)
    ipb_auto: Col[int] = col()
    ipb_anon_only: Col[int] = col()
    ipb_create_account: Col[int] = col()
    ipb_enable_autoblock: Col[int] = col()
    ipb_expiry: Col[str] = col(BinaryDecoder)
    ipb_range_start: Col[str] = col(BinaryDecoder)
    ipb_range_end: Col[str] = col(BinaryDecoder)
    ipb_deleted: Col[int] = col()
    ipb_block_email: Col[int] = col()
    ipb_allow_usertalk: Col[int] = col()
    ipb_parent_block_id: Col[int] = col()
    ipb_sitewide: Col[int] = col()


class IpblocksRestrictions(Base):
    """The table ``ipblocks_restrictions``.

    Attributes:
        ir_ipb_id: ``int``
        ir_type: ``int``
        ir_value: ``int``
    """

    __tablename__ = "ipblocks_restrictions"
    ir_ipb_id: Col[int] = col(primary_key=True)
    ir_type: Col[int] = col(primary_key=True)
    ir_value: Col[int] = col(primary_key=True)


class Iwlinks(Base):
    """The table ``iwlinks``.

    Attributes:
        iwl_from: ``int``
        iwl_prefix: ``str``
        iwl_title: ``str``
    """

    __tablename__ = "iwlinks"
    iwl_from: Col[int] = col(primary_key=True)
    iwl_prefix: Col[str] = col(BinaryDecoder, primary_key=True)
    iwl_title: Col[str] = col(BinaryDecoder, primary_key=True)


class Job(Base):
    """The table ``job``.

    Attributes:
        job_id: ``int``
        job_cmd: ``str``
        job_namespace: ``int``
        job_title: ``str``
        job_timestamp: ``str``
        job_params: ``str``
        job_random: ``int``
        job_attempts: ``int``
        job_token: ``str``
        job_token_timestamp: ``str``
        job_sha1: ``str``
    """

    __tablename__ = "job"
    job_id: Col[int] = col(primary_key=True)
    job_cmd: Col[str] = col(BinaryDecoder)
    job_namespace: Col[int] = col()
    job_title: Col[str] = col(BinaryDecoder)
    job_timestamp: Col[str] = col(BinaryDecoder)
    job_params: Col[str] = col(BinaryDecoder)
    job_random: Col[int] = col()
    job_attempts: Col[int] = col()
    job_token: Col[str] = col(BinaryDecoder)
    job_token_timestamp: Col[str] = col(BinaryDecoder)
    job_sha1: Col[str] = col(BinaryDecoder)


class L10nCache(Base):
    """The table ``l10n_cache``.

    Attributes:
        lc_lang: ``str``
        lc_key: ``str``
        lc_value: ``str``
    """

    __tablename__ = "l10n_cache"
    lc_lang: Col[str] = col(BinaryDecoder, primary_key=True)
    lc_key: Col[str] = col(BinaryDecoder, primary_key=True)
    lc_value: Col[str] = col(BinaryDecoder)


class Langlinks(Base):
    """The table ``langlinks``.

    Attributes:
        ll_from: ``int``
        ll_lang: ``str``
        ll_title: ``str``
    """

    __tablename__ = "langlinks"
    ll_from: Col[int] = col(primary_key=True)
    ll_lang: Col[str] = col(BinaryDecoder, primary_key=True)
    ll_title: Col[str] = col(BinaryDecoder)


class Linktarget(Base):
    """The table ``linktarget``.

    Attributes:
        lt_id: ``int``
        lt_namespace: ``int``
        lt_title: ``str``
    """

    __tablename__ = "linktarget"
    lt_id: Col[int] = col(primary_key=True)
    lt_namespace: Col[int] = col()
    lt_title: Col[str] = col(BinaryDecoder)


class LogSearch(Base):
    """The table ``log_search``.

    Attributes:
        ls_field: ``str``
        ls_value: ``str``
        ls_log_id: ``int``
    """

    __tablename__ = "log_search"
    ls_field: Col[str] = col(BinaryDecoder, primary_key=True)
    ls_value: Col[str] = col(BinaryDecoder, primary_key=True)
    ls_log_id: Col[int] = col(primary_key=True)


class Logging(Base):
    """The table ``logging``.

    Attributes:
        log_id: ``int``
        log_type: ``str``
        log_action: ``str``
        log_timestamp: ``str``
        log_actor: ``Decimal``
        log_namespace: ``int``
        log_title: ``str``
        log_page: ``int``
        log_comment_id: ``Decimal``
        log_params: ``str``
        log_deleted: ``int``
    """

    __tablename__ = "logging"
    log_id: Col[int] = col(primary_key=True)
    log_type: Col[str] = col(BinaryDecoder)
    log_action: Col[str] = col(BinaryDecoder)
    log_timestamp: Col[str] = col(BinaryDecoder)
    log_actor: Col[Decimal] = col()
    log_namespace: Col[int] = col()
    log_title: Col[str] = col(BinaryDecoder)
    log_page: Col[int] = col()
    log_comment_id: Col[Decimal] = col()
    log_params: Col[str] = col(BinaryDecoder)
    log_deleted: Col[int] = col()


class ModuleDeps(Base):
    """The table ``module_deps``.

    Attributes:
        md_module: ``str``
        md_skin: ``str``
        md_deps: ``str``
    """

    __tablename__ = "module_deps"
    md_module: Col[str] = col(BinaryDecoder, primary_key=True)
    md_skin: Col[str] = col(BinaryDecoder, primary_key=True)
    md_deps: Col[str] = col(BinaryDecoder)


class Objectcache(Base):
    """The table ``objectcache``.

    Attributes:
        keyname: ``str``
        value: ``str``
        exptime: ``str``
        modtoken: ``str``
        flags: ``int``
    """

    __tablename__ = "objectcache"
    keyname: Col[str] = col(BinaryDecoder, primary_key=True)
    value: Col[str] = col(BinaryDecoder)
    exptime: Col[str] = col(BinaryDecoder)
    modtoken: Col[str] = col(BinaryDecoder)
    flags: Col[int] = col()


class Oldimage(Base):
    """The table ``oldimage``.

    Attributes:
        oi_name: ``str``
        oi_archive_name: ``str``
        oi_size: ``int``
        oi_width: ``int``
        oi_height: ``int``
        oi_bits: ``int``
        oi_description_id: ``Decimal``
        oi_actor: ``int``
        oi_timestamp: ``str``
        oi_metadata: ``str``
        oi_media_type: ``str``
        oi_major_mime: ``str``
        oi_minor_mime: ``str``
        oi_deleted: ``int``
        oi_sha1: ``str``
    """

    __tablename__ = "oldimage"
    oi_name: Col[str] = col(BinaryDecoder, primary_key=True)
    oi_archive_name: Col[str] = col(BinaryDecoder, primary_key=True)
    oi_size: Col[int] = col(primary_key=True)
    oi_width: Col[int] = col(primary_key=True)
    oi_height: Col[int] = col(primary_key=True)
    oi_bits: Col[int] = col(primary_key=True)
    oi_description_id: Col[Decimal] = col(primary_key=True)
    oi_actor: Col[int] = col(primary_key=True)
    oi_timestamp: Col[str] = col(BinaryDecoder, primary_key=True)
    oi_metadata: Col[str] = col(BinaryDecoder, primary_key=True)
    oi_media_type: Col[str] = col(BinaryDecoder, primary_key=True)
    oi_major_mime: Col[str] = col(BinaryDecoder, primary_key=True)
    oi_minor_mime: Col[str] = col(BinaryDecoder, primary_key=True)
    oi_deleted: Col[int] = col(primary_key=True)
    oi_sha1: Col[str] = col(BinaryDecoder, primary_key=True)


class Page(Base):
    """The table ``page``.

    Attributes:
        page_id: ``int``
        page_namespace: ``int``
        page_title: ``str``
        page_is_redirect: ``int``
        page_is_new: ``int``
        page_random: ``float``
        page_touched: ``str``
        page_links_updated: ``str``
        page_latest: ``int``
        page_len: ``int``
        page_content_model: ``str``
        page_lang: ``str``
    """

    __tablename__ = "page"
    page_id: Col[int] = col(primary_key=True)
    page_namespace: Col[int] = col()
    page_title: Col[str] = col(BinaryDecoder)
    page_is_redirect: Col[int] = col()
    page_is_new: Col[int] = col()
    page_random: Col[float] = col()
    page_touched: Col[str] = col(BinaryDecoder)
    page_links_updated: Col[str] = col(BinaryDecoder)
    page_latest: Col[int] = col()
    page_len: Col[int] = col()
    page_content_model: Col[str] = col(BinaryDecoder)
    page_lang: Col[str] = col(BinaryDecoder)


class PageProps(Base):
    """The table ``page_props``.

    Attributes:
        pp_page: ``int``
        pp_propname: ``str``
        pp_value: ``str``
        pp_sortkey: ``float``
    """

    __tablename__ = "page_props"
    pp_page: Col[int] = col(primary_key=True)
    pp_propname: Col[str] = col(BinaryDecoder, primary_key=True)
    pp_value: Col[str] = col(BinaryDecoder)
    pp_sortkey: Col[float] = col()


class PageRestrictions(Base):
    """The table ``page_restrictions``.

    Attributes:
        pr_id: ``int``
        pr_page: ``int``
        pr_type: ``str``
        pr_level: ``str``
        pr_cascade: ``int``
        pr_expiry: ``str``
    """

    __tablename__ = "page_restrictions"
    pr_id: Col[int] = col(primary_key=True)
    pr_page: Col[int] = col()
    pr_type: Col[str] = col(BinaryDecoder)
    pr_level: Col[str] = col(BinaryDecoder)
    pr_cascade: Col[int] = col()
    pr_expiry: Col[str] = col(BinaryDecoder)


class Pagelinks(Base):
    """The table ``pagelinks``.

    Attributes:
        pl_from: ``int``
        pl_from_namespace: ``int``
        pl_target_id: ``int``
    """

    __tablename__ = "pagelinks"
    pl_from: Col[int] = col(primary_key=True)
    pl_from_namespace: Col[int] = col()
    pl_target_id: Col[int] = col()


class ProtectedTitles(Base):
    """The table ``protected_titles``.

    Attributes:
        pt_namespace: ``int``
        pt_title: ``str``
        pt_user: ``int``
        pt_reason_id: ``int``
        pt_timestamp: ``str``
        pt_expiry: ``str``
        pt_create_perm: ``str``
    """

    __tablename__ = "protected_titles"
    pt_namespace: Col[int] = col(primary_key=True)
    pt_title: Col[str] = col(BinaryDecoder, primary_key=True)
    pt_user: Col[int] = col()
    pt_reason_id: Col[int] = col()
    pt_timestamp: Col[str] = col(BinaryDecoder)
    pt_expiry: Col[str] = col(BinaryDecoder)
    pt_create_perm: Col[str] = col(BinaryDecoder)


class Querycache(Base):
    """The table ``querycache``.

    Attributes:
        qc_type: ``str``
        qc_value: ``int``
        qc_namespace: ``int``
        qc_title: ``str``
    """

    __tablename__ = "querycache"
    qc_type: Col[str] = col(BinaryDecoder, primary_key=True)
    qc_value: Col[int] = col(primary_key=True)
    qc_namespace: Col[int] = col(primary_key=True)
    qc_title: Col[str] = col(BinaryDecoder, primary_key=True)


class QuerycacheInfo(Base):
    """The table ``querycache_info``.

    Attributes:
        qci_type: ``str``
        qci_timestamp: ``str``
    """

    __tablename__ = "querycache_info"
    qci_type: Col[str] = col(BinaryDecoder, primary_key=True)
    qci_timestamp: Col[str] = col(BinaryDecoder)


class Querycachetwo(Base):
    """The table ``querycachetwo``.

    Attributes:
        qcc_type: ``str``
        qcc_value: ``int``
        qcc_namespace: ``int``
        qcc_title: ``str``
        qcc_namespacetwo: ``int``
        qcc_titletwo: ``str``
    """

    __tablename__ = "querycachetwo"
    qcc_type: Col[str] = col(BinaryDecoder, primary_key=True)
    qcc_value: Col[int] = col(primary_key=True)
    qcc_namespace: Col[int] = col(primary_key=True)
    qcc_title: Col[str] = col(BinaryDecoder, primary_key=True)
    qcc_namespacetwo: Col[int] = col(primary_key=True)
    qcc_titletwo: Col[str] = col(BinaryDecoder, primary_key=True)


class Recentchanges(Base):
    """The table ``recentchanges``.

    Attributes:
        rc_id: ``int``
        rc_timestamp: ``str``
        rc_actor: ``Decimal``
        rc_namespace: ``int``
        rc_title: ``str``
        rc_comment_id: ``int``
        rc_minor: ``int``
        rc_bot: ``int``
        rc_new: ``int``
        rc_cur_id: ``int``
        rc_this_oldid: ``int``
        rc_last_oldid: ``int``
        rc_type: ``int``
        rc_source: ``str``
        rc_patrolled: ``int``
        rc_ip: ``str``
        rc_old_len: ``int``
        rc_new_len: ``int``
        rc_deleted: ``int``
        rc_logid: ``int``
        rc_log_type: ``str``
        rc_log_action: ``str``
        rc_params: ``str``
    """

    __tablename__ = "recentchanges"
    rc_id: Col[int] = col(primary_key=True)
    rc_timestamp: Col[str] = col(BinaryDecoder)
    rc_actor: Col[Decimal] = col()
    rc_namespace: Col[int] = col()
    rc_title: Col[str] = col(BinaryDecoder)
    rc_comment_id: Col[int] = col()
    rc_minor: Col[int] = col()
    rc_bot: Col[int] = col()
    rc_new: Col[int] = col()
    rc_cur_id: Col[int] = col()
    rc_this_oldid: Col[int] = col()
    rc_last_oldid: Col[int] = col()
    rc_type: Col[int] = col()
    rc_source: Col[str] = col(BinaryDecoder)
    rc_patrolled: Col[int] = col()
    rc_ip: Col[str] = col(BinaryDecoder)
    rc_old_len: Col[int] = col()
    rc_new_len: Col[int] = col()
    rc_deleted: Col[int] = col()
    rc_logid: Col[int] = col()
    rc_log_type: Col[str] = col(BinaryDecoder)
    rc_log_action: Col[str] = col(BinaryDecoder)
    rc_params: Col[str] = col(BinaryDecoder)


class Redirect(Base):
    """The table ``redirect``.

    Attributes:
        rd_from: ``int``
        rd_namespace: ``int``
        rd_title: ``str``
        rd_interwiki: ``str``
        rd_fragment: ``str``
    """

    __tablename__ = "redirect"
    rd_from: Col[int] = col(primary_key=True)
    rd_namespace: Col[int] = col()
    rd_title: Col[str] = col(BinaryDecoder)
    rd_interwiki: Col[str] = col(BinaryDecoder)
    rd_fragment: Col[str] = col(BinaryDecoder)


class Revision(Base):
    """The table ``revision``.

    Attributes:
        rev_id: ``int``
        rev_page: ``int``
        rev_comment_id: ``int``
        rev_actor: ``int``
        rev_timestamp: ``str``
        rev_minor_edit: ``int``
        rev_deleted: ``int``
        rev_len: ``int``
        rev_parent_id: ``int``
        rev_sha1: ``str``
    """

    __tablename__ = "revision"
    rev_id: Col[int] = col(primary_key=True)
    rev_page: Col[int] = col()
    rev_comment_id: Col[int] = col()
    rev_actor: Col[int] = col()
    rev_timestamp: Col[str] = col(BinaryDecoder)
    rev_minor_edit: Col[int] = col()
    rev_deleted: Col[int] = col()
    rev_len: Col[int] = col()
    rev_parent_id: Col[int] = col()
    rev_sha1: Col[str] = col(BinaryDecoder)


class Searchindex(Base):
    """The table ``searchindex``.

    Attributes:
        si_page: ``int``
        si_title: ``str``
        si_text: ``str``
    """

    __tablename__ = "searchindex"
    si_page: Col[int] = col(primary_key=True)
    si_title: Col[str] = col(BinaryDecoder)
    si_text: Col[str] = col(BinaryDecoder)


class SiteIdentifiers(Base):
    """The table ``site_identifiers``.

    Attributes:
        si_type: ``str``
        si_key: ``str``
        si_site: ``int``
    """

    __tablename__ = "site_identifiers"
    si_type: Col[str] = col(BinaryDecoder, primary_key=True)
    si_key: Col[str] = col(BinaryDecoder, primary_key=True)
    si_site: Col[int] = col()


class SiteStats(Base):
    """The table ``site_stats``.

    Attributes:
        ss_row_id: ``int``
        ss_total_edits: ``int``
        ss_good_articles: ``int``
        ss_total_pages: ``int``
        ss_users: ``int``
        ss_active_users: ``int``
        ss_images: ``int``
    """

    __tablename__ = "site_stats"
    ss_row_id: Col[int] = col(primary_key=True)
    ss_total_edits: Col[int] = col()
    ss_good_articles: Col[int] = col()
    ss_total_pages: Col[int] = col()
    ss_users: Col[int] = col()
    ss_active_users: Col[int] = col()
    ss_images: Col[int] = col()


class Sites(Base):
    """The table ``sites``.

    Attributes:
        site_id: ``int``
        site_global_key: ``str``
        site_type: ``str``
        site_group: ``str``
        site_source: ``str``
        site_language: ``str``
        site_protocol: ``str``
        site_domain: ``str``
        site_data: ``str``
        site_forward: ``int``
        site_config: ``str``
    """

    __tablename__ = "sites"
    site_id: Col[int] = col(primary_key=True)
    site_global_key: Col[str] = col(BinaryDecoder)
    site_type: Col[str] = col(BinaryDecoder)
    site_group: Col[str] = col(BinaryDecoder)
    site_source: Col[str] = col(BinaryDecoder)
    site_language: Col[str] = col(BinaryDecoder)
    site_protocol: Col[str] = col(BinaryDecoder)
    site_domain: Col[str] = col(BinaryDecoder)
    site_data: Col[str] = col(BinaryDecoder)
    site_forward: Col[int] = col()
    site_config: Col[str] = col(BinaryDecoder)


class SlotRoles(Base):
    """The table ``slot_roles``.

    Attributes:
        role_id: ``int``
        role_name: ``str``
    """

    __tablename__ = "slot_roles"
    role_id: Col[int] = col(primary_key=True)
    role_name: Col[str] = col(BinaryDecoder)


class Slots(Base):
    """The table ``slots``.

    Attributes:
        slot_revision_id: ``int``
        slot_role_id: ``int``
        slot_content_id: ``int``
        slot_origin: ``int``
    """

    __tablename__ = "slots"
    slot_revision_id: Col[int] = col(primary_key=True)
    slot_role_id: Col[int] = col(primary_key=True)
    slot_content_id: Col[int] = col()
    slot_origin: Col[int] = col()


class Templatelinks(Base):
    """The table ``templatelinks``.

    Attributes:
        tl_from: ``int``
        tl_from_namespace: ``int``
        tl_target_id: ``int``
    """

    __tablename__ = "templatelinks"
    tl_from: Col[int] = col(primary_key=True)
    tl_from_namespace: Col[int] = col()
    tl_target_id: Col[int] = col(primary_key=True)


class Text(Base):
    """The table ``text``.

    Attributes:
        old_id: ``int``
        old_text: ``str``
        old_flags: ``str``
    """

    __tablename__ = "text"
    old_id: Col[int] = col(primary_key=True)
    old_text: Col[str] = col(BinaryDecoder)
    old_flags: Col[str] = col(BinaryDecoder)


class Updatelog(Base):
    """The table ``updatelog``.

    Attributes:
        ul_key: ``str``
        ul_value: ``str``
    """

    __tablename__ = "updatelog"
    ul_key: Col[str] = col(BinaryDecoder, primary_key=True)
    ul_value: Col[str] = col(BinaryDecoder)


class Uploadstash(Base):
    """The table ``uploadstash``.

    Attributes:
        us_id: ``int``
        us_user: ``int``
        us_key: ``str``
        us_orig_path: ``str``
        us_path: ``str``
        us_source_type: ``str``
        us_timestamp: ``str``
        us_status: ``str``
        us_chunk_inx: ``int``
        us_props: ``str``
        us_size: ``int``
        us_sha1: ``str``
        us_mime: ``str``
        us_media_type: ``str``
        us_image_width: ``int``
        us_image_height: ``int``
        us_image_bits: ``int``
    """

    __tablename__ = "uploadstash"
    us_id: Col[int] = col(primary_key=True)
    us_user: Col[int] = col()
    us_key: Col[str] = col(BinaryDecoder)
    us_orig_path: Col[str] = col(BinaryDecoder)
    us_path: Col[str] = col(BinaryDecoder)
    us_source_type: Col[str] = col(BinaryDecoder)
    us_timestamp: Col[str] = col(BinaryDecoder)
    us_status: Col[str] = col(BinaryDecoder)
    us_chunk_inx: Col[int] = col()
    us_props: Col[str] = col(BinaryDecoder)
    us_size: Col[int] = col()
    us_sha1: Col[str] = col(BinaryDecoder)
    us_mime: Col[str] = col(BinaryDecoder)
    us_media_type: Col[str] = col(BinaryDecoder)
    us_image_width: Col[int] = col()
    us_image_height: Col[int] = col()
    us_image_bits: Col[int] = col()


class User(Base):
    """The table ``user``.

    Attributes:
        user_id: ``int``
        user_name: ``str``
        user_real_name: ``str``
        user_password: ``str``
        user_newpassword: ``str``
        user_newpass_time: ``str``
        user_email: ``str``
        user_touched: ``str``
        user_token: ``str``
        user_email_authenticated: ``str``
        user_email_token: ``str``
        user_email_token_expires: ``str``
        user_registration: ``str``
        user_editcount: ``int``
        user_password_expires: ``str``
        user_is_temp: ``int``
    """

    __tablename__ = "user"
    user_id: Col[int] = col(primary_key=True)
    user_name: Col[str] = col(BinaryDecoder)
    user_real_name: Col[str] = col(BinaryDecoder)
    user_password: Col[str] = col(BinaryDecoder)
    user_newpassword: Col[str] = col(BinaryDecoder)
    user_newpass_time: Col[str] = col(BinaryDecoder)
    user_email: Col[str] = col(BinaryDecoder)
    user_touched: Col[str] = col(BinaryDecoder)
    user_token: Col[str] = col(BinaryDecoder)
    user_email_authenticated: Col[str] = col(BinaryDecoder)
    user_email_token: Col[str] = col(BinaryDecoder)
    user_email_token_expires: Col[str] = col(BinaryDecoder)
    user_registration: Col[str] = col(BinaryDecoder)
    user_editcount: Col[int] = col()
    user_password_expires: Col[str] = col(BinaryDecoder)
    user_is_temp: Col[int] = col()


class UserAutocreateSerial(Base):
    """The table ``user_autocreate_serial``.

    Attributes:
        uas_shard: ``int``
        uas_year: ``int``
        uas_value: ``int``
    """

    __tablename__ = "user_autocreate_serial"
    uas_shard: Col[int] = col(primary_key=True)
    uas_year: Col[int] = col(primary_key=True)
    uas_value: Col[int] = col()


class UserFormerGroups(Base):
    """The table ``user_former_groups``.

    Attributes:
        ufg_user: ``int``
        ufg_group: ``str``
    """

    __tablename__ = "user_former_groups"
    ufg_user: Col[int] = col(primary_key=True)
    ufg_group: Col[str] = col(BinaryDecoder, primary_key=True)


class UserGroups(Base):
    """The table ``user_groups``.

    Attributes:
        ug_user: ``int``
        ug_group: ``str``
        ug_expiry: ``str``
    """

    __tablename__ = "user_groups"
    ug_user: Col[int] = col(primary_key=True)
    ug_group: Col[str] = col(BinaryDecoder, primary_key=True)
    ug_expiry: Col[str] = col(BinaryDecoder)


class UserNewtalk(Base):
    """The table ``user_newtalk``.

    Attributes:
        user_id: ``int``
        user_ip: ``str``
        user_last_timestamp: ``str``
    """

    __tablename__ = "user_newtalk"
    user_id: Col[int] = col(primary_key=True)
    user_ip: Col[str] = col(BinaryDecoder, primary_key=True)
    user_last_timestamp: Col[str] = col(BinaryDecoder, primary_key=True)


class UserProperties(Base):
    """The table ``user_properties``.

    Attributes:
        up_user: ``int``
        up_property: ``str``
        up_value: ``str``
    """

    __tablename__ = "user_properties"
    up_user: Col[int] = col(primary_key=True)
    up_property: Col[str] = col(BinaryDecoder, primary_key=True)
    up_value: Col[str] = col(BinaryDecoder)


class Watchlist(Base):
    """The table ``watchlist``.

    Attributes:
        wl_id: ``int``
        wl_user: ``int``
        wl_namespace: ``int``
        wl_title: ``str``
        wl_notificationtimestamp: ``str``
    """

    __tablename__ = "watchlist"
    wl_id: Col[int] = col(primary_key=True)
    wl_user: Col[int] = col()
    wl_namespace: Col[int] = col()
    wl_title: Col[str] = col(BinaryDecoder)
    wl_notificationtimestamp: Col[str] = col(BinaryDecoder)


class WatchlistExpiry(Base):
    """The table ``watchlist_expiry``.

    Attributes:
        we_item: ``int``
        we_expiry: ``str``
    """

    __tablename__ = "watchlist_expiry"
    we_item: Col[int] = col(primary_key=True)
    we_expiry: Col[str] = col(BinaryDecoder)


class WbChanges(Base):
    """The table ``wb_changes``.

    Attributes:
        change_id: ``int``
        change_type: ``str``
        change_time: ``str``
        change_object_id: ``str``
        change_revision_id: ``int``
        change_user_id: ``int``
        change_info: ``str``
    """

    __tablename__ = "wb_changes"
    change_id: Col[int] = col(primary_key=True)
    change_type: Col[str] = col(BinaryDecoder)
    change_time: Col[str] = col(BinaryDecoder)
    change_object_id: Col[str] = col(BinaryDecoder)
    change_revision_id: Col[int] = col()
    change_user_id: Col[int] = col()
    change_info: Col[str] = col(BinaryDecoder)


class WbChangesSubscription(Base):
    """The table ``wb_changes_subscription``.

    Attributes:
        cs_row_id: ``int``
        cs_entity_id: ``str``
        cs_subscriber_id: ``str``
    """

    __tablename__ = "wb_changes_subscription"
    cs_row_id: Col[int] = col(primary_key=True)
    cs_entity_id: Col[str] = col(BinaryDecoder)
    cs_subscriber_id: Col[str] = col(BinaryDecoder)


class WbIdCounters(Base):
    """The table ``wb_id_counters``.

    Attributes:
        id_value: ``int``
        id_type: ``str``
    """

    __tablename__ = "wb_id_counters"
    id_value: Col[int] = col(primary_key=True)
    id_type: Col[str] = col(BinaryDecoder, primary_key=True)


class WbItemsPerSite(Base):
    """The table ``wb_items_per_site``.

    Attributes:
        ips_row_id: ``int``
        ips_item_id: ``int``
        ips_site_id: ``str``
        ips_site_page: ``str``
    """

    __tablename__ = "wb_items_per_site"
    ips_row_id: Col[int] = col(primary_key=True)
    ips_item_id: Col[int] = col()
    ips_site_id: Col[str] = col(BinaryDecoder)
    ips_site_page: Col[str] = col(BinaryDecoder)


class WbPropertyInfo(Base):
    """The table ``wb_property_info``.

    Attributes:
        pi_property_id: ``int``
        pi_type: ``str``
        pi_info: ``str``
    """

    __tablename__ = "wb_property_info"
    pi_property_id: Col[int] = col(primary_key=True)
    pi_type: Col[str] = col(BinaryDecoder)
    pi_info: Col[str] = col(BinaryDecoder)


class WbtItemTerms(Base):
    """The table ``wbt_item_terms``.

    Attributes:
        wbit_id: ``int``
        wbit_item_id: ``int``
        wbit_term_in_lang_id: ``int``
    """

    __tablename__ = "wbt_item_terms"
    wbit_id: Col[int] = col(primary_key=True)
    wbit_item_id: Col[int] = col()
    wbit_term_in_lang_id: Col[int] = col()


class WbtPropertyTerms(Base):
    """The table ``wbt_property_terms``.

    Attributes:
        wbpt_id: ``int``
        wbpt_property_id: ``int``
        wbpt_term_in_lang_id: ``int``
    """

    __tablename__ = "wbt_property_terms"
    wbpt_id: Col[int] = col(primary_key=True)
    wbpt_property_id: Col[int] = col()
    wbpt_term_in_lang_id: Col[int] = col()


class WbtTermInLang(Base):
    """The table ``wbt_term_in_lang``.

    Attributes:
        wbtl_id: ``int``
        wbtl_type_id: ``int``
        wbtl_text_in_lang_id: ``int``
    """

    __tablename__ = "wbt_term_in_lang"
    wbtl_id: Col[int] = col(primary_key=True)
    wbtl_type_id: Col[int] = col()
    wbtl_text_in_lang_id: Col[int] = col()


class WbtTextInLang(Base):
    """The table ``wbt_text_in_lang``.

    Attributes:
        wbxl_id: ``int``
        wbxl_language: ``str``
        wbxl_text_id: ``int``
    """

    __tablename__ = "wbt_text_in_lang"
    wbxl_id: Col[int] = col(primary_key=True)
    wbxl_language: Col[str] = col(BinaryDecoder)
    wbxl_text_id: Col[int] = col()


class WbtType(Base):
    """The table ``wbt_type``.

    Attributes:
        wby_id: ``int``
        wby_name: ``str``
    """

    __tablename__ = "wbt_type"
    wby_id: Col[int] = col(primary_key=True)
    wby_name: Col[str] = col(BinaryDecoder)


class WbtText(Base):
    """The table ``wbt_text``.

    Attributes:
        wbx_id: ``int``
        wbx_text: ``str``
    """

    __tablename__ = "wbt_text"
    wbx_id: Col[int] = col(primary_key=True)
    wbx_text: Col[str] = col(BinaryDecoder)


class PageAssessments(Base):
    """The table ``page_assessments``.

    Attributes:
        pa_page_id: ``int``
        pa_project_id: ``int``
        pa_class: ``str``
        pa_importance: ``str``
        pa_page_revision: ``int``
    """

    __tablename__ = "page_assessments"
    pa_page_id: Col[int] = col(primary_key=True)
    pa_project_id: Col[int] = col(primary_key=True)
    pa_class: Col[str] = col(BinaryDecoder)
    pa_importance: Col[str] = col(BinaryDecoder)
    pa_page_revision: Col[int] = col()


class PageAssessmentsProjects(Base):
    """The table ``page_assessments_projects``.

    Attributes:
        pap_project_id: ``int``
        pap_project_title: ``str``
        pap_parent_id: ``int``
    """

    __tablename__ = "page_assessments_projects"
    pap_project_id: Col[int] = col(primary_key=True)
    pap_project_title: Col[str] = col(BinaryDecoder)
    pap_parent_id: Col[int] = col()
