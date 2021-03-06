from django.db import models
from django.contrib.contenttypes.models import ContentType
try:
    from django.contrib.contenttypes.fields import GenericRelation
except ImportError:  # Django < 1.9 pragma: no cover
    from django.contrib.contenttypes.generic import GenericRelation
from reversion.models import Revision


class TestModelGenericInline(models.Model):

    object_id = models.IntegerField()

    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
    )

    inline_name = models.CharField(
        max_length=191,
        default="v1",
    )


class TestModel(models.Model):

    name = models.CharField(
        max_length=191,
        default="v1",
    )

    related = models.ManyToManyField(
        "TestModelRelated",
        blank=True,
        related_name="+",
    )

    related_through = models.ManyToManyField(
        "TestModelRelated",
        blank=True,
        through="TestModelThrough",
        related_name="+",
    )

    generic_inlines = GenericRelation(TestModelGenericInline)


class TestModelEscapePK(models.Model):

    name = models.CharField(max_length=191, primary_key=True)


class TestModelThrough(models.Model):

    test_model = models.ForeignKey(
        "TestModel",
        related_name="+",
        on_delete=models.CASCADE,
    )

    test_model_related = models.ForeignKey(
        "TestModelRelated",
        related_name="+",
        on_delete=models.CASCADE,
    )

    name = models.CharField(
        max_length=191,
        default="v1",
    )


class TestModelRelated(models.Model):

    name = models.CharField(
        max_length=191,
        default="v1",
    )


class TestModelParent(TestModel):

    parent_name = models.CharField(
        max_length=191,
        default="parent v1",
    )


class TestModelInline(models.Model):

    test_model = models.ForeignKey(
        TestModel,
        on_delete=models.CASCADE,
    )

    inline_name = models.CharField(
        max_length=191,
        default="v1",
    )


class TestModelNestedInline(models.Model):
    test_model_inline = models.ForeignKey(
        TestModelInline,
        on_delete=models.CASCADE,
    )

    nested_inline_name = models.CharField(
        max_length=191,
        default="v1",
    )


class TestMeta(models.Model):

    revision = models.ForeignKey(
        Revision,
        on_delete=models.CASCADE,
    )

    name = models.CharField(
        max_length=191,
    )
