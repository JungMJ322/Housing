# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Competition(models.Model):
    area_grade = models.TextField(db_column='AREA_GRADE', blank=True, null=True)  # Field name made lowercase.
    avr_score = models.TextField(db_column='AVR_SCORE', blank=True, null=True)  # Field name made lowercase.
    bottom_score = models.TextField(db_column='BOTTOM_SCORE', blank=True, null=True)  # Field name made lowercase.
    compet_rate = models.TextField(db_column='COMPET_RATE', blank=True, null=True)  # Field name made lowercase.
    house_manage_no = models.IntegerField(db_column='HOUSE_MANAGE_NO')  # Field name made lowercase.
    model_no = models.TextField(db_column='MODEL_NO', blank=True, null=True)  # Field name made lowercase.
    top_score = models.TextField(db_column='TOP_SCORE', blank=True, null=True)  # Field name made lowercase.
    total_req = models.TextField(db_column='TOTAL_REQ', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'competition'


class DetailChange(models.Model):
    address = models.TextField(db_column='ADDRESS', blank=True, null=True)  # Field name made lowercase.
    build_comp = models.TextField(db_column='BUILD_COMP', blank=True, null=True)  # Field name made lowercase.
    house_manage_no = models.IntegerField(db_column='HOUSE_MANAGE_NO', blank=True, null=True)  # Field name made lowercase.
    house_name = models.TextField(db_column='HOUSE_NAME', blank=True, null=True)  # Field name made lowercase.
    house_secd = models.TextField(db_column='HOUSE_SECD', blank=True, null=True)  # Field name made lowercase.
    imprmn_bsns_at = models.TextField(db_column='IMPRMN_BSNS_AT', blank=True, null=True)  # Field name made lowercase.
    lat = models.TextField(db_column='LAT', blank=True, null=True)  # Field name made lowercase.
    lot = models.TextField(db_column='LOT', blank=True, null=True)  # Field name made lowercase.
    lrscl_bldlnd_at = models.TextField(db_column='LRSCL_BLDLND_AT', blank=True, null=True)  # Field name made lowercase.
    mdat_trget_area_secd = models.TextField(db_column='MDAT_TRGET_AREA_SECD', blank=True, null=True)  # Field name made lowercase.
    place_code = models.TextField(db_column='PLACE_CODE', blank=True, null=True)  # Field name made lowercase.
    rent_secd = models.TextField(db_column='RENT_SECD', blank=True, null=True)  # Field name made lowercase.
    speclt_rdn_earth_at = models.TextField(db_column='SPECLT_RDN_EARTH_AT', blank=True, null=True)  # Field name made lowercase.
    start_receipt = models.TextField(db_column='START_RECEIPT', blank=True, null=True)  # Field name made lowercase.
    supply_size = models.IntegerField(db_column='SUPPLY_SIZE', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'detail_change'


class Park(models.Model):
    id = models.IntegerField(primary_key=True)
    park_name = models.TextField(blank=True, null=True)
    park_type = models.TextField(blank=True, null=True)
    start_date = models.TextField(blank=True, null=True)
    place = models.TextField(blank=True, null=True)
    lat = models.TextField(blank=True, null=True)
    lot = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'park'
