"""A module to decode text strings based on an encoding.

This is typically used by the Data Manager's API instance methods
when launching applications (and Jobs) where text requires decoding,
given a 'template' string and a 'dictionary' of parameters and values.
"""
import enum
import os
import re
from typing import Any, Dict, List, Optional, Pattern, Tuple

import jsonschema
import yaml

# The decoding engine implementations.
# The modules are expected to be called 'decode_<TextEncoding.lower()>'
from . import decode_jinja2_3_0

# The (built-in) schemas...
# from the same directory as us.
_JD_SCHEMA_FILE: str = os.path.join(
    os.path.dirname(__file__), "job-definition-schema.yaml"
)
_MANIFEST_SCHEMA_FILE: str = os.path.join(
    os.path.dirname(__file__), "manifest-schema.yaml"
)

# Load the JD schema YAML file now.
# This must work as the file is installed along with this module.
assert os.path.isfile(_JD_SCHEMA_FILE)
with open(_JD_SCHEMA_FILE, "r", encoding="utf8") as schema_file:
    _JOB_DEFINITION_SCHEMA: Dict[str, Any] = yaml.load(
        schema_file, Loader=yaml.FullLoader
    )
assert _JOB_DEFINITION_SCHEMA

# Load the Manifest schema YAML file now.
# This must work as the file is installed along with this module.
assert os.path.isfile(_MANIFEST_SCHEMA_FILE)
with open(_MANIFEST_SCHEMA_FILE, "r", encoding="utf8") as schema_file:
    _MANIFEST_SCHEMA: Dict[str, Any] = yaml.load(schema_file, Loader=yaml.FullLoader)
assert _MANIFEST_SCHEMA

REPO_TYPE_GITHUB: str = "github"
REPO_TYPE_GITLAB: str = "gitlab"
_REPO_TYPES: List[str] = [REPO_TYPE_GITHUB, REPO_TYPE_GITLAB]

_GITHUB_REF_RE: Pattern[str] = re.compile(r"/([^/]+)/data-manager/")


class TextEncoding(enum.Enum):
    """A general text encoding format, used initially for Job text fields."""

    JINJA2_3_0 = 1  # Encoding that complies with Jinja2 v3.0.x


def validate_manifest_schema(manifest: Dict[str, Any]) -> Optional[str]:
    """Checks the Job Definition Manifest (a preloaded job-definition dictionary)
    against the built-in schema. If there's an error the error text is
    returned, otherwise None.
    """
    assert isinstance(manifest, dict)

    # Validate the Manifest against our schema
    try:
        jsonschema.validate(manifest, schema=_MANIFEST_SCHEMA)
    except jsonschema.ValidationError as ex:
        return str(ex.message)

    # OK if we get here
    return None


def validate_job_schema(job_definition: Dict[str, Any]) -> Optional[str]:
    """Checks the Job Definition (a preloaded job-definition dictionary)
    against the built-in schema. If there's an error the error text is
    returned, otherwise None.
    """
    assert isinstance(job_definition, dict)

    # Validate the Job Definition against our schema
    try:
        jsonschema.validate(job_definition, schema=_JOB_DEFINITION_SCHEMA)
    except jsonschema.ValidationError as ex:
        return str(ex.message)

    # OK if we get here
    return None


def get_supported_repository_types() -> List[str]:
    """Returns a copy of the supported Git repository types."""
    return _REPO_TYPES[:]


def _get_github_job_doc_url(
    manifest_url: str, collection: str, job_id: str, doc_url: Optional[str]
) -> str:
    """Returns the path to the 'pretty' doc for a GitHub public reference,
    based on the manifest URL, collection and Job ID.
    """
    manifest_directory_url, _ = os.path.split(manifest_url)
    if doc_url and not doc_url.startswith("https://"):
        # doc-url defined but does not start 'https://'
        # the doc_url is a path within the docs directory
        doc_url = f"{manifest_directory_url}/docs/{doc_url}"
    elif doc_url is None:
        # No doc-url.
        # The doc is expected to be in 'docs',
        # as '{job}.md' in the {collection} directory.
        doc_url = f"{manifest_directory_url}/docs/{collection}/{job_id}.md"
    else:
        # How did we get here?
        assert False

    # The doc-url here is to the 'raw' file.
    # Adjust it so that it should refer to the 'pretty' file.
    #
    # We replace:
    #
    # - raw.githubusercontent.com with github.com
    # - The field prior to 'data-manager' (the branch/tag) with '/blob/(field)
    doc_url = doc_url.replace("raw.githubusercontent.com", "github.com", 1)
    ref_match = _GITHUB_REF_RE.search(doc_url)
    assert ref_match
    original_ref = ref_match[0]
    ref = ref_match[1]
    new_ref: str = f"/blob/{ref}/data-manager/"
    doc_url = doc_url.replace(original_ref, new_ref, 1)

    return doc_url


def _get_gitlab_job_doc_url(
    manifest_url: str, collection: str, job_id: str, doc_url: Optional[str]
) -> str:
    """Returns the path to the doc for a GitLab reference,
    based on the manifest URL, collection and Job ID.
    """
    manifest_directory_url, _ = manifest_url.split("%2f")
    if doc_url and not doc_url.startswith("https://"):
        # doc-url defined but does not start 'https://'
        # the doc_url is a path within the docs directory
        doc_url = doc_url.replace("/", "%2f")
        doc_url = f"{manifest_directory_url}%2fdocs%2f{doc_url}/raw"
    elif doc_url is None:
        # No doc-url.
        # The doc is expected to be in 'docs',
        # as '{job}.md' in the {collection} directory.
        doc_url = f"{manifest_directory_url}%2fdocs%2f{collection}%2f{job_id}.md/raw"
    else:
        # How did we get here?
        assert False

    return doc_url


def get_job_doc_url(
    repo_type: str,
    collection: str,
    job: str,
    job_definition: Dict[str, Any],
    manifest_url: str,
) -> str:
    """Returns the Job's documentation URL for a specific Job using the JOb's
    'doc-url' and manifest URL. The job manifest is expected to
    have been validated, and we expect to have been given one job structure
    from the job's definition, not the whole job definition file.

    repo_type must be one of the supported types.
    """
    assert repo_type in _REPO_TYPES
    assert collection
    assert job
    assert isinstance(job_definition, dict)
    assert manifest_url

    # The response depends on the value of 'doc-url'.
    # 1. If there is no doc-url the URL is auto-generated
    #    from the manifest URL, job collection and job name.
    # 2. If the doc-url begins 'https://' then this is taken as the doc-url
    # 3. If the doc-url does not begin https:// then is
    #    assumed to be relative to the manifest directory URL

    # A typical GitHub manifest URL will look like this...
    #
    #   https://raw.githubusercontent.com/InformaticsMatters/
    #       virtual-screening/main/data-manager/manifest-virtual-screening.yaml
    #
    # And, in this case the base for an auto-generated doc-url (if we need it)
    # will be: -
    #
    #   https://raw.githubusercontent.com/InformaticsMatters/
    #       virtual-screening/main/data-manager/docs

    doc_url: Optional[str] = job_definition.get("doc-url", None)

    # If doc-url starts 'https://' just return it
    if doc_url and doc_url.startswith("https://"):
        return doc_url
    if doc_url is not None:
        assert not doc_url.startswith("/")
        assert not doc_url.endswith("/")

    if repo_type == REPO_TYPE_GITHUB:
        doc_url = _get_github_job_doc_url(manifest_url, collection, job, doc_url)
    elif repo_type == REPO_TYPE_GITLAB:
        doc_url = _get_gitlab_job_doc_url(manifest_url, collection, job, doc_url)

    assert doc_url
    return doc_url


def decode(
    template_text: str,
    variable_map: Optional[Dict[str, str]],
    subject: str,
    template_engine: TextEncoding,
) -> Tuple[str, bool]:
    """Given some text and a 'variable map' (a dictionary of keys and values)
    this returns the decoded text (using the named engine) as a string
    and a boolean set to True. On failure the boolean is False and the returned
    string is an error message.

    The 'subject' is a symbolic reference to the text
    used for error reporting so the client understands what text is
    in error. i.e. if the text is for a 'command'
    the subject might be 'command'.
    """
    assert template_text
    assert subject
    assert template_engine

    # If there are no variables just return the template text
    if variable_map is None:
        return template_text, True

    if template_engine.name.lower() == "jinja2_3_0":
        return decode_jinja2_3_0.decode(template_text, variable_map, subject)

    # Unsupported engine if we get here!
    return f"Unsupported template engine: {template_engine}", False
