"""rev_io tap class."""

from typing import List

from singer_sdk import Tap, Stream
from singer_sdk import typing as th  # JSON schema typing helpers

from tap_rev_io.streams import (
    InventoryItemStream, AddressesStream, AgentsStream, AnnouncementsStream,
    AuditsStream, BillProfilesStream, BillsStream, ChargesStream,
    ContactsStream, ContactTypesStream, CreditsStream, CustomerRelationshipsStream,
    CustomersStream, InventoryTypesStream, NotesStream,
    NotesTypesStream, OrdersStream, OrderServiceProductsStream, OrderServicesStream,
    PackageProductsStream, PackagesStream, PaymentAccountsStream, PaymentMethodsStream,
    PaymentsStream, ProcessesStream, ProcessPhasesStream, ProcessTasksStream,
    ProductGroupsStream, ProductsStream, ProductTypesStream, ProviderAccountsStream,
    ProvidersStream, ReportCategoriesStream, ReportsStream, RequestAddressesStream,
    RequestContactsStream, RequestProductsStream, RequestsStream, RequestServicesStream,
    RequestStatusesStream, RequestTemplatesStream, ServiceInventoryStream, ServiceProductStream,
    ServicesStream, ServiceTypesStream, TasksStream, TaskStepsStream,
    TaskTypesStream, TicketJournalsStream, TicketProcessesStream, TicketsStream,
    UsagePlanGroupsStream, UserGroupsStream, UsersStream

)

STREAM_TYPES = [
    InventoryItemStream, 
    AddressesStream, 
    AgentsStream, AnnouncementsStream,
    AuditsStream, BillProfilesStream, BillsStream, ChargesStream,
    ContactsStream, ContactTypesStream, CreditsStream, CustomerRelationshipsStream,
    CustomersStream, InventoryTypesStream, NotesStream, NotesTypesStream,
    OrdersStream, OrderServiceProductsStream, OrderServicesStream, PackageProductsStream,
    PackagesStream, PaymentAccountsStream, PaymentMethodsStream, PaymentsStream,
    ProcessesStream, ProcessPhasesStream, ProcessTasksStream,
    ProductGroupsStream, ProductsStream, ProductTypesStream, ProviderAccountsStream,
    ProvidersStream, ReportCategoriesStream, ReportsStream, RequestAddressesStream,
    RequestContactsStream, RequestProductsStream, RequestsStream, RequestServicesStream,
    RequestStatusesStream, RequestTemplatesStream, ServiceInventoryStream, ServiceProductStream,
    ServicesStream, ServiceTypesStream, TasksStream, TaskStepsStream,
    TaskTypesStream, TicketJournalsStream, TicketProcessesStream,
    TicketsStream, UsagePlanGroupsStream, UserGroupsStream, UsersStream
]


class Taprev_io(Tap):
    """rev_io tap class."""
    name = "tap-rev_io"

    config_jsonschema = th.PropertiesList(
        th.Property(
            "username",
            th.StringType,
            required=True,
            description="Username to connect to the API"
        ),
        th.Property(
            "password",
            th.StringType,
            required=True,
            description="Password to connect to the API"
        ),
        th.Property(
            "page_size",
            th.IntegerType,
            default=500,
            description="The page size to extract"
        ),
    ).to_dict()

    def discover_streams(self) -> List[Stream]:
        """Return a list of discovered streams."""
        return [stream_class(tap=self) for stream_class in STREAM_TYPES]
