from dataclasses import dataclass
from typing import *
import typing

__all__ = ['PropertyValue', 'Place', 'Location', 'PersonIdentifier', 'Organization', 'Person', 'Thing', 'PersonOrThing',
           'Event', 'EventSet', 'CID', 'get_fragments']


@dataclass(order=True)
class BaseDictKey:
    """
    Inheriting from this class is identical to making each field Optional and None by default
    """

    def __init_subclass__(cls, *args, **kwargs):
        for field, value in cls.__annotations__.items():
            cls.__annotations__[field] = typing.Union[value, None]
            if not hasattr(cls, field):
                setattr(cls, field, None)
        super().__init_subclass__(*args, **kwargs)


@dataclass
class PropertyValue:
    name: str
    value: str

    @staticmethod
    def gql_fragment():
        return """
            fragment propsFields on PropertyValue {
              name
              value
            }
            """


@dataclass
class Place(BaseDictKey):
    streetAddress: str
    city: str
    state: str
    postalCode: str
    country: str
    countryCode: str
    latitude: float
    longitude: float
    url: str

    @staticmethod
    def gql_fragment():
        return """
            fragment placeFields on Place {
              streetAddress
              city
              state
              postalCode
              country
              countryCode
              latitude
              longitude
              url
            }
            """


@dataclass
class Location(BaseDictKey):
    artifact: str
    representation: str
    card: str
    coherenceGraph: str
    artifactArchivalCopy: str

    @staticmethod
    def gql_fragment():
        return """
            fragment locationFields on Location {
              representation
              artifact
              card
              coherenceGraph
              artifactArchivalCopy
            }
            """


@dataclass
class PersonIdentifier(BaseDictKey):
    ORCID: str
    ISNI: str
    Twitter: str
    Other: str

    @staticmethod
    def gql_fragment():
        return """
            fragment personIdentifierFields on PersonIdentifier {
              ORCID
              ISNI
              Twitter
              Other
            }
            """


@dataclass
class Organization(BaseDictKey):
    identifier: PropertyValue
    name: str
    where: Place
    image: str

    @staticmethod
    def gql_fragment():
        return """
            fragment organizationFields on Organization {
              identifier {
                name
                value
              }
              name
              where {
                ...placeFields
              }
              image
            }
            """


@dataclass
class Person(BaseDictKey):
    identifier: PersonIdentifier
    name: str
    givenName: str
    additionalName: str
    familyName: str
    honorificPrefix: str
    honorificSuffix: str
    alternateName: str
    email: str
    image: str
    jobTitle: str
    department: Organization
    worksFor: Organization

    @staticmethod
    def gql_fragment():
        return """
            fragment personFields on Person {
              identifier {
                ...personIdentifierFields
              }
              name
              givenName
              familyName
              additionalName
              alternateName
              honorificPrefix
              honorificSuffix
              email
              jobTitle
              department {
                ...organizationFields
              }
              worksFor {
                ...organizationFields
              }
              image
            }
            """


@dataclass
class Thing(BaseDictKey):
    identifier: PropertyValue
    name: str
    image: str

    @staticmethod
    def gql_fragment():
        return """
            fragment thingFields on Thing {
              identifier {
                ...propsFields
              }
              name
              image
            }
            """


@dataclass
class PersonOrThing(BaseDictKey):
    person: Person
    thing: Thing

    @staticmethod
    def gql_fragment():
        return """
            fragment personOrThingFields on PersonOrThing {
              person {
                ...personFields
              }
              thing {
                ...thingFields
              }
            }
            """


@dataclass
class Event(BaseDictKey):
    who: PersonOrThing
    what: Thing
    where: Place
    when: str
    location: Location
    props: List[PropertyValue]

    @staticmethod
    def gql_fragment():
        return """
        fragment eventFields on Event {
              who {
                ...personOrThingFields
              }
              what {
                ...thingFields
              }
              where {
                ...placeFields
              }
              when
              location {
                ...locationFields
              }
              props {
                ...propsFields
              }
            }
            """


@dataclass
class CIDEvent(BaseDictKey):
    who: PersonOrThing
    what: Thing
    where: Place
    when: str
    location: Location
    props: List[PropertyValue]
    text: Text

    @staticmethod
    def gql_fragment(text_fields=None):
        allowed_fields = ['rawText', 'documentMetadata', 'summary', 'keyTerms', 'entities', 'sectionedText',
                          'frontMatter', 'backMatter', 'hasFullText']
        fields = '\n'.join([f for f in text_fields if f in allowed_fields]) if text_fields else None
        return """
            fragment cidEventFields on CIDEvent {
                  who {
                    ...personOrThingFields
                  }
                  what {
                    ...thingFields
                  }
                  where {
                    ...placeFields
                  }
                  when
                  location {
                    ...locationFields
                  }
                  props {
                    ...propsFields
                  }
                """ + (f"""
                  text {{
                     {fields}
                  }}
                }}
                """ if fields else "}")


@dataclass
class EventSet(BaseDictKey):
    CID: Event
    ARK: Event
    DOI: Event
    MARC: Event
    PARENT: Event

    @staticmethod
    def gql_fragment():
        return """
                fragment eventSetFields on EventSet {
                  CID {
                    ...cidEventFields
                  }
                  PARENT {
                    ...eventFields
                  }
                  ARK {
                    ...eventFields
                  }
                  DOI {
                    ...eventFields
                  }
                  MARC {
                    ...eventFields
                  }
                }
            """


@dataclass
class CID(BaseDictKey):
    cid: str
    events: EventSet

    @staticmethod
    def gql_fragment():
        return """
            fragment cidFields on CID {
              cid
              events {
                ...eventSetFields
              }
            }
        """


def get_fragments(text_fields=None):
    return f"""
        {PersonIdentifier.gql_fragment()}
        {Place.gql_fragment()}
        {Organization.gql_fragment()}
        {Person.gql_fragment()}
        {Thing.gql_fragment()}
        {Location.gql_fragment()}
        {PropertyValue.gql_fragment()}
        {PersonOrThing.gql_fragment()}
        {Event.gql_fragment()}
        {CIDEvent.gql_fragment(text_fields)}
        {EventSet.gql_fragment()}
        {CID.gql_fragment()}
    """
