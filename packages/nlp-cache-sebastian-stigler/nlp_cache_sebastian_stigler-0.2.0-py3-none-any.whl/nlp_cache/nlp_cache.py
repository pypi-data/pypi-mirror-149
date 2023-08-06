import glob
import os.path
import spacy
import hashlib

from typing import Iterable, Dict, Any, Optional


class NlpCache:
    """A cached text-processing pipeline."""

    def __init__(
        self,
        uncached_nlp: spacy.language.Language,
        path: str,
    ) -> None:
        """Initialize a cached text-processing pipeline.

        uncached_nlp (spacy.language.Language): Fallback text-processing pipeline
            which should be used if the object is called with a unknown text.
        path (str): The path to the cache.
        RETURNS (NoneType): None
        """
        if not os.path.isdir(path):
            raise OSError(f"Path '{path}' does not exist.")
        self.uncached_nlp = uncached_nlp
        self.path = path
        self._doc = self.uncached_nlp("")

    def __call__(
        self,
        text: str,
        *,
        disable: Iterable[str] = spacy.util.SimpleFrozenList(),
        component_cfg: Optional[Dict[str, Dict[str, Any]]] = None,
    ) -> spacy.tokens.doc.Doc:
        """Apply the pipeline to some text. The text can span multiple sentences,
        and can contain arbitrary whitespace. Alignment into the original string
        is preserved. If the text was already processed once, it will be loaded
        from the cache.
        text (str): The text to be processed.
        disable (List[str]): Names of the pipeline components to disable.
        component_cfg (Dict[str, dict]): An optional dictionary with extra
            keyword arguments for specific components.
        RETURNS (Doc): A container for accessing the annotations.
        """
        hashsum = hashlib.sha512(text.encode()).hexdigest()
        doc_file = self._create_path(hashsum, 0)
        if os.path.exists(doc_file):
            potential_files = glob.glob(doc_file[:-1] + "*")
            for filename in potential_files:
                doc = self._doc.copy().from_disk(filename)
                if doc.text == text:
                    return doc
            else:
                return self._create_and_cache_doc(
                    text, hashsum, len(potential_files), disable=disable, component_cfg=component_cfg
                )
        return self._create_and_cache_doc(
            text, hashsum, 0, disable=disable, component_cfg=component_cfg
        )

    def _create_and_cache_doc(
        self,
        text: str,
        hashsum: str,
        idx: int,
        *,
        disable: Iterable[str] = spacy.util.SimpleFrozenList(),
        component_cfg: Optional[Dict[str, Dict[str, Any]]] = None,
    ) -> spacy.tokens.doc.Doc:
        """Helper method creates a new `Doc` and add it to the cache.
        text (str): The text to be processed.
        hashsum (str): Sha512 of `text`.
        disable (List[str]): Names of the pipeline components to disable.
        component_cfg (Dict[str, dict]): An optional dictionary with extra
            keyword arguments for specific components.
        RETURNS (Doc): A container for accessing the annotations.
        """
        doc_file = self._create_path(hashsum, idx)
        doc = self.uncached_nlp(text, disable=disable, component_cfg=component_cfg)
        doc.to_disk(doc_file)
        return doc

    def _create_path(self, hashsum: str, idx: int) -> str:
        """Helper method to create the path to the cache file.
        hashsum (str): Sha512 of `text` to be used as filename.
        idx (int): index of `text` in the bucked with the given `hashsum`
            (collision management).
        RETURN (str): The path to the cache file.
        """
        basename = f"{hashsum}-{idx}"
        path1, path2, path3, path4, filename = basename[:2], basename[2:4], basename[4:6], basename[6:8],  basename[8:]
        path = os.path.join(self.path, path1, path2, path3, path4)
        os.makedirs(path, mode=0o755, exist_ok=True)
        return os.path.join(path, filename)
