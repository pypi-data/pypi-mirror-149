import typing
from nubium_schemas import dc, pdc, AvroModel


def _eloqua_hash_field(*args, **kwargs):
    kwargs["metadata"] = kwargs.get("metadata", {})
    kwargs["metadata"]["eloqua_hash"] = True
    return dc.field(*args, **kwargs)


@pdc
class Address(AvroModel):
    class Meta:
        schema_doc = False

    country_name: str = _eloqua_hash_field(default="")
    country_code: str = _eloqua_hash_field(default="")
    address_street_1: str = _eloqua_hash_field(default="")
    address_street_2: str = _eloqua_hash_field(default="")
    address_street_3: str = _eloqua_hash_field(default="")
    address_city: str = _eloqua_hash_field(default="")
    address_state_province: str = _eloqua_hash_field(default="")
    address_postal_code: str = _eloqua_hash_field(default="")
    core_based_statistical_area: str = _eloqua_hash_field(default="")
    combined_statistical_area: str = _eloqua_hash_field(default="")


@pdc
class Job(AvroModel):
    class Meta:
        schema_doc = False

    company: str = _eloqua_hash_field(default="")
    business_phone: str = _eloqua_hash_field(default="")
    job_title: str = _eloqua_hash_field(default="")
    department: str = _eloqua_hash_field(default="")
    job_role: str = _eloqua_hash_field(default="")
    job_level: str = _eloqua_hash_field(default="")
    job_function: str = _eloqua_hash_field(default="")
    industry: str = _eloqua_hash_field(default="")
    annual_revenue: str = _eloqua_hash_field(default="")
    company_size: str = _eloqua_hash_field(default="")


@pdc
class PersonalFacts(AvroModel):
    class Meta:
        schema_doc = False
        alias_nested_items = {
            "address": "Address",
            "job": "Job",
        }

    email_address: str = _eloqua_hash_field()
    salutation: str = _eloqua_hash_field(default="")
    first_name: str = _eloqua_hash_field(default="")
    last_name: str = _eloqua_hash_field(default="")
    mobile_phone: str = _eloqua_hash_field(default="")
    language_preference: str = _eloqua_hash_field(default="")
    address: Address = dc.field(default_factory=Address)
    job: Job = dc.field(default_factory=Job)


@pdc
class Mlsm(AvroModel):
    class Meta:
        schema_doc = False

    lead_ranking: str = _eloqua_hash_field(default="")
    lead_rating: str = _eloqua_hash_field(default="")
    interest_level: str = _eloqua_hash_field(default="")
    qualification_level: str = _eloqua_hash_field(default="")
    all_scores: str = _eloqua_hash_field(default="")


@pdc
class LeadScore(AvroModel):
    class Meta:
        schema_doc = False
        alias_nested_items = {"mlsm": "Mlsm"}

    mlsm: Mlsm = dc.field(default_factory=Mlsm)


@pdc
class MarketingDescriptors(AvroModel):
    class Meta:
        schema_doc = False
        alias_nested_items = {"lead_score": "LeadScore"}

    persona: str = _eloqua_hash_field(default="")
    super_region: str = _eloqua_hash_field(default="")
    sub_region: str = _eloqua_hash_field(default="")
    penalty_box_reason: str = ""
    penalty_box_expiration: str = _eloqua_hash_field(default="")
    lead_score: LeadScore = dc.field(default_factory=LeadScore)


@pdc
class Privacy(AvroModel):
    class Meta:
        schema_doc = False

    consent_email_marketing: str = _eloqua_hash_field(default="")
    consent_email_marketing_timestamp: str = ""
    consent_email_marketing_source: str = ""
    consent_share_to_partner: str = ""
    consent_share_to_partner_timestamp: str = ""
    consent_share_to_partner_source: str = ""
    consent_phone_marketing: str = ""
    consent_phone_marketing_timestamp: str = ""
    consent_phone_marketing_source: str = ""


@pdc
class OptIn(AvroModel):
    class Meta:
        schema_doc = False

    f_formdata_optin: str = ""
    f_formdata_optin_phone: str = ""
    f_formdata_sharetopartner: str = ""


@pdc
class Location(AvroModel):
    class Meta:
        schema_doc = False

    city_from_ip: str = ""
    state_province_from_ip: str = ""
    postal_code_from_ip: str = ""
    country_from_ip: str = _eloqua_hash_field(default="")
    country_from_dns: str = _eloqua_hash_field(default="")


@pdc
class LastSubmission(AvroModel):
    class Meta:
        schema_doc = False
        alias_nested_items = {"opt_in": "OptIn", "location": "Location"}

    submission_date: str = ""
    submission_source: str = ""
    opt_in: OptIn = dc.field(default_factory=OptIn)
    location: Location = dc.field(default_factory=Location)


@pdc
class SfdcLeadId(AvroModel):
    class Meta:
        schema_doc = False

    lead_id: str = ""
    record_status: str = ""


@pdc
class SfdcContactId(AvroModel):
    class Meta:
        schema_doc = False

    contact_id: str = ""
    account_id: str = ""
    record_status: str = ""


@pdc
class Tombstone(AvroModel):
    class Meta:
        schema_doc = False

    is_tombstoned: str = ""
    tombstone_timestamp: str = ""
    tombstone_source: str = ""
    delete_all_data: str = ""


@pdc
class TrackingIds(AvroModel):
    class Meta:
        schema_doc = False
        alias_nested_items = {"sfdc_lead_id": "SfdcLeadId", "sfdc_contact_id": "SfdcContactId"}

    eloqua_contact_id: str = _eloqua_hash_field(default="")
    sfdc_lead_ids: typing.List[SfdcLeadId] = dc.field(default_factory=lambda: [SfdcLeadId().asdict()])
    sfdc_contact_ids: typing.List[SfdcContactId] = dc.field(default_factory=lambda: [SfdcContactId().asdict()])
