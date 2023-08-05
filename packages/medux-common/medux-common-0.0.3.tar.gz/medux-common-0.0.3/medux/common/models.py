import uuid

from django.contrib.auth.models import AbstractUser
from django.contrib.sites.models import Site
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class AutoDateTimeField(models.DateTimeField):
    def pre_save(self, model_instance, add):
        return timezone.now()


class CreatedModifiedModel(models.Model):
    """A simple mixin for model classes that need to have created/modified fields."""

    created = models.DateTimeField(editable=False, default=timezone.now)
    modified = AutoDateTimeField(default=timezone.now)

    class Meta:
        abstract = True


class SoftDeletionQuerySet(models.QuerySet):
    def delete(self):
        return super().update(deleted_at=timezone.now())

    def hard_delete(self):
        return super().delete()

    def alive(self):
        return self.filter(deleted_at=None)

    def dead(self):
        return self.exclude(deleted_at=None)


class SoftDeletionManager(models.Manager):
    """Custom Django Manager for soft-delete queries.

    This object manager transparently only fetches objects from the
    database that are not soft-deleted."""

    # https://medium.com/@adriennedomingus/soft-deletion-in-django-e4882581c340
    def __init__(self, *args, **kwargs):
        self.alive_only = kwargs.pop("alive_only", True)
        super().__init__(*args, **kwargs)

    def get_queryset(self):
        if self.alive_only:
            return SoftDeletionQuerySet(self.model).filter(deleted_at=None)
        return SoftDeletionQuerySet(self.model)

    def hard_delete(self):
        return self.get_queryset().hard_delete()


class BaseModel(CreatedModifiedModel):
    """An abstract base class with common used functions.

    Every relevant model that needs soft_deletion in MedUX should inherit BaseModel.

    It provides:
    * basic created/modified timestamps for auditing
    * a soft delete functionality: Deleted items are just marked as deleted.
    """

    deleted_at = models.DateTimeField(
        editable=False, blank=True, null=True, default=None
    )

    row_version = models.PositiveIntegerField(editable=False, default=0)

    # The standard manager only returns not-soft-deleted objects
    objects = SoftDeletionManager()

    # The all_objects Manager returns ALL objects, even soft-deleted ones
    all_objects = SoftDeletionManager(alive_only=False)

    class Meta:
        abstract = True

    def delete(self, using=None, keep_parents=False):
        self.deleted_at = timezone.now()
        self.save()

    def hard_delete(self):
        super().delete()


SEX = (("m", _("male")), ("f", _("female")))


class Tenant(models.Model):
    """A MedUX tenant, like an MD who "owns" a homepage, or a MedUX appliance."""

    class Meta:
        verbose_name = _("Tenant")
        verbose_name_plural = _("Tenants")

    uuid = models.UUIDField(default=uuid.uuid4, unique=True)

    title = models.CharField(max_length=50, blank=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    sex = models.CharField(max_length=1, choices=SEX)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=30, blank=True)
    email = models.EmailField(unique=True, default="", blank=True, null=True)

    @property
    def name(self):
        # TODO: if user exists, take his name.
        return f"{self.last_name}, {self.first_name}"

    def __str__(self):
        return f"{self.name}"


class User(AbstractUser):
    """Custom MedUX User model.

    A user usually belongs to a tenant, except for e.g. admin users.
    """

    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, null=True)


class TenantSite(Site):
    """A site that belongs to a tenant.

    This model is meant to be subclassed by sites that need a common tenant.

    The `tenantedsite` is added as attribute to each request.
    """

    class Meta:
        verbose_name = _("Tenant aware site")
        verbose_name_plural = _("Tenant aware sites")

    tenant = models.ForeignKey(
        Tenant,
        verbose_name=_("Tenant"),
        on_delete=models.CASCADE,
        help_text=_("Tenant this site is belonging to"),
        default=None,
    )

    # alias_of = models.ForeignKey(
    #     "TenantSite",
    #     blank=True,
    #     null=True,
    #     on_delete=models.SET_NULL,
    #     help_text=_("If this site is just an alias site, provide the main site here."),
    # )

    @property
    def subdomain(self) -> str | None:
        """:returns: subdomain, if applicable, else None"""

        parts = self.domain.split(".")
        if len(parts) == 3:
            return parts[0]
        else:
            return None

    @property
    def slug(self):
        return self.domain.replace(".", "_")


class TenantMixin(models.Model):
    """A mixin that can be added to a model to mark it as belonging to a tenant.

    It adds a "tenant" ForeignKey to the model."""

    class Meta:
        abstract = True

    # change to ForeignKey if a tenant should manage more >1 homepages later?
    tenant = models.ForeignKey(
        Tenant,
        verbose_name=_("Tenant"),
        on_delete=models.CASCADE,
    )
