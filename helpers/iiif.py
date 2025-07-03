from dataclasses import dataclass
import functools
from typing import Dict, List, Union
import requests
from requests.adapters import HTTPAdapter
from urllib3.util import Retry


@dataclass
class IIIFImageItem:
    base_url: str
    width: Union[int, None] = None
    height: Union[int, None] = None
    label: Union[str, None] = None
    show_rendering: bool = True
    sapa_uri: Union[str, None] = None


def get_manifest_base_metadata(
    copyright=None, rights="http://creativecommons.org/licenses/by-sa/4.0/"
):
    return recursive_filter_none(
        {
            "@context": "http://iiif.io/api/presentation/3/context.json",
            "type": "Manifest",
            "rights": rights,
            "homepage": [
                {
                    "id": "https://sapa.swiss",
                    "type": "Text",
                    "label": {"en": ["SAPA Homepage"]},
                    "format": "text/html",
                }
            ],
            "requiredStatement": value_if_not_none(
                copyright,
                {
                    "label": create_multilingual("Copyright"),
                    "value": create_multilingual(copyright),
                },
            ),
            "provider": [
                {
                    "id": "https://www.wikidata.org/entity/Q50920401",
                    "type": "Agent",
                    "label": {
                        "en": ["SAPA, Swiss Archive of the Performing Arts"],
                        "de": [
                            "Stiftung SAPA, Schweizer Archiv der Darstellenden Künste"
                        ],
                        "fr": ["Fondation SAPA, Archives suisses des arts de la scène"],
                        "it": [
                            "Fondazione SAPA, Archivio svizzero delle arti della scena"
                        ],
                    },
                    "homepage": [
                        {
                            "id": "https://sapa.swiss/",
                            "type": "Text",
                            "label": {
                                "en": [
                                    "The SAPA Foundation, Swiss Archive of the Performing Arts, collects documents and objects of importance to the history of the performing arts and makes them accessible to a wider audience."
                                ],
                                "de": [
                                    "Die Stiftung SAPA, Schweizer Archiv der Darstellenden Künste, sammelt Dokumente und Objekte, die für die Geschichte der Darstellenden Künste bedeutsam sind, und stellt diese einem breiten Publikum zur Verfügung."
                                ],
                                "fr": [
                                    "La Fondation SAPA, Archives suisses des arts de la scène, collecte et met à disposition de tous les publics les documents et objets constituant l‘histoire des arts de la scène en Suisse. Sa mission: préserver les traces de ces arts éphémères et complexes pour les transmettre aux générations futures."
                                ],
                                "it": [
                                    "SAPA raccoglie e mette a disposizione del pubblico documenti e oggetti di rilevanza storica per le arti sceniche in Svizzera. La Fondazione si pone l’obiettivo di preservare le tracce di queste arti effimere e complesse per tramandarle alle generazioni future."
                                ],
                            },
                            "format": "text/html",
                        }
                    ],
                    "logo": [
                        {
                            "id": "https://memobase.ch/sites/default/files/2021-05/sap-logo.jpg",
                            "type": "Image",
                            "format": "image/jpeg",
                            "height": 100,
                            "width": 260,
                        }
                    ],
                }
            ],
            "viewingDirection": "left-to-right",
        }
    )


def create_manifest(
    manifest_base_url: str,
    items: List[any],
    base_metadata: any,
    thumbnail_iiif_base_url=None,
    label=None,
    summary=None,
    sapa_resource=None,
    sapa_resource_label=None,
    identifier=None,
    description=None,
    creator=None,
):
    if len(items) <= 0:
        raise ValueError("There must be at least one image to create a manifest")
    return recursive_filter_none(
        base_metadata
        | {
            "id": f"{manifest_base_url}.json",
            "label": create_multilingual(label),
            "summary": create_multilingual(summary),
            "seeAlso": [
                value_if_not_none(
                    sapa_resource,
                    {
                        "id": sapa_resource,
                        "type": "Text",
                        "label": {
                            "en": [
                                sapa_resource_label
                                if sapa_resource_label is not None
                                else "Record on Swiss Performing Arts Platform"
                            ]
                        },
                        "format": "text/html",
                    },
                )
            ],
            "metadata": [
                value_if_not_none(
                    identifier,
                    {
                        "label": {
                            "en": ["Identifier"],
                            "de": ["Signatur"],
                            "fr": ["Cote"],
                            "it": ["Segnatura"],
                        },
                        "value": create_multilingual(identifier),
                    },
                ),
                value_if_not_none(
                    description,
                    {
                        "label": {
                            "en": ["Description"],
                            "de": ["Beschreibung"],
                            "fr": ["Description"],
                            "it": ["Descrizione"],
                        },
                        "value": create_multilingual(description),
                    },
                ),
            ]
            + prepare_metadata(
                creator,
                {
                    "en": ["Creator"],
                    "de": ["Urheber"],
                    "fr": ["Auteur"],
                    "it": ["Autore"],
                },
            ),
            "thumbnail": value_if_not_none(
                thumbnail_iiif_base_url,
                [
                    {
                        "id": f"{thumbnail_iiif_base_url}/full/80,/0/default.jpg",
                        "type": "Image",
                        "format": "image/jpeg",
                        "service": [
                            {
                                "id": thumbnail_iiif_base_url,
                                "type": "ImageService3",
                                "profile": "level2",
                            }
                        ],
                    }
                ],
            ),
            "items": items,
        }
    )


def prepare_metadata(value: str | List | Dict | None, label: str | Dict):
    if isinstance(value, str) or isinstance(value, dict):
        return [
            {"label": create_multilingual(label), "value": create_multilingual(value)}
        ]
    elif isinstance(value, list):
        return [
            {"label": create_multilingual(label), "value": create_multilingual(val)}
            for val in value
        ]
    else:
        return [None]


def create_manifest_from_iiif_images(
    manifest_base_url: str,
    iiif_images: List[IIIFImageItem],
    base_metadata: any,
    label=None,
    summary=None,
    sapa_resource=None,
    sapa_resource_label=None,
    identifier=None,
    description=None,
    creator=None,
):
    if len(iiif_images) <= 0:
        raise ValueError("There must be at least one image to create a manifest")
    items = [
        create_image_item(iiif_image, index + 1, manifest_base_url)
        for (index, iiif_image) in enumerate(iiif_images)
    ]
    return create_manifest(
        manifest_base_url,
        items,
        base_metadata,
        iiif_images[0].base_url,
        label,
        summary,
        sapa_resource,
        sapa_resource_label,
        identifier,
        description,
        creator,
    )


def create_image_item(iiif_image: IIIFImageItem, index, manifest_base_url):
    iiif_base_url = iiif_image.base_url
    manifest_base_url = remove_trailing_slash(manifest_base_url)
    iiif_base_url = remove_trailing_slash(iiif_base_url)

    if iiif_image.height is None or iiif_image.width is None:
        width, height = iiif_base_url_to_size(iiif_base_url)
    else:
        width, height = iiif_image.width, iiif_image.height

    if width is None or height is None:
        return None

    canvas_url = f"{manifest_base_url}/p{index:03d}"
    return {
        "id": canvas_url,
        "type": "Canvas",
        "height": int(height),
        "width": int(width),
        "label": (
            create_multilingual(iiif_image.label)
            if iiif_image.label
            else create_multilingual(
                {
                    "de": f"Bild {index}",
                    "fr": f"Image {index}",
                    "en": f"Picture {index}",
                    "it": f"Immagine {index}",
                }
            )
        ),
        "thumbnail": [
            {
                "id": f"{iiif_base_url}/full/!300,300/0/default.jpg",
                "type": "Image",
                "format": "image/jpeg",
                "height": 300,
                "width": 300,
                "service": [
                    {
                        "id": iiif_base_url,
                        "type": "ImageService3",
                        "profile": "level2",
                    }
                ],
            }
        ],
        "rendering": [
            value_if_not_none(
                iiif_image.show_rendering if iiif_image.show_rendering else None,
                (
                    {
                        "id": f"{iiif_base_url}/full/max/0/default.jpg",
                        "type": "Image",
                        "label": create_multilingual(
                            {
                                "de": "Bild",
                                "fr": "Image",
                                "en": "Picture",
                                "it": "Immagine",
                            }
                        ),
                        "format": "image/jpeg",
                    }
                    if iiif_image.show_rendering
                    else None
                ),
            ),
            value_if_not_none(
                iiif_image.sapa_uri,
                {
                    "id": iiif_image.sapa_uri,
                    "type": "Text",
                    "label": {"en": ["Record on Swiss performing arts platform"]},
                    "format": "text/html",
                },
            ),
        ],
        "seeAlso": value_if_not_none(
            iiif_image.sapa_uri,
            [
                {
                    "id": iiif_image.sapa_uri,
                    "type": "Text",
                    "label": {"none": ["Record on Swiss performing arts platform"]},
                    "format": "text/html",
                }
            ],
        ),
        "items": [
            {
                "id": f"{canvas_url}/1",
                "type": "AnnotationPage",
                "items": [
                    {
                        "id": f"{manifest_base_url}/annotation/p{index:03d}-image",
                        "type": "Annotation",
                        "motivation": "painting",
                        "body": {
                            "id": f"{iiif_base_url}/full/max/0/default.jpg",
                            "type": "Image",
                            "format": "image/jpeg",
                            "height": int(height),
                            "width": int(width),
                            "service": [
                                {
                                    "id": iiif_base_url,
                                    "profile": "level1",
                                    "type": "ImageService3",
                                }
                            ],
                        },
                        "target": f"{canvas_url}/1",
                    }
                ],
            }
        ],
    }


s = requests.Session()

retries = Retry(total=5, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504])

s.mount("https://", HTTPAdapter(max_retries=retries))


def iiif_base_url_to_size(iiif_base_url: str):
    iiif_url = remove_trailing_slash(iiif_base_url) + "/info.json"
    try:
        res = s.get(iiif_url)
        if res.status_code == 404:
            print(f"Error with {iiif_url}, it does not exists")
            return None, None
        res.raise_for_status()
        res_json = res.json()
        return (int(res_json["width"]), int(res_json["height"]))
    except Exception as e:
        print(f"Error with {iiif_url}: ", e)
        return None, None


def create_multilingual(
    value: Union[None, str, Dict[str, str]], languages=["en", "de", "fr", "it"]
):
    if value is None:
        return None
    elif isinstance(value, str):
        return {language: [value] for language in languages}
    else:
        return {language: [val] for language, val in value.items()}


def recursive_filter_none(item):
    if isinstance(item, list):
        new_list = [
            x
            for x in (recursive_filter_none(x) for x in item)
            if x not in [None, [], {}]
        ]
        return new_list if new_list else None
    elif isinstance(item, dict):
        new_dict = {
            k: v
            for k, v in ((k, recursive_filter_none(v)) for k, v in item.items())
            if v not in [None, [], {}]
        }
        return new_dict if new_dict else None
    else:
        return item


def value_if_not_none(input_, value):
    if input_ is not None:
        return value
    else:
        return None


def remove_trailing_slash(url):
    return url.rstrip("/")
