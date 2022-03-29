# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Busstop(models.Model):
    id = models.BigIntegerField(primary_key=True)
    lat = models.TextField(blank=True, null=True)
    lot = models.TextField(blank=True, null=True)
    stn_name = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'busStop'


class Competition(models.Model):
    area_grade = models.TextField(db_column='AREA_GRADE', blank=True, null=True)  # Field name made lowercase.
    avr_score = models.BigIntegerField(db_column='AVR_SCORE', blank=True, null=True)  # Field name made lowercase.
    bottom_score = models.BigIntegerField(db_column='BOTTOM_SCORE', blank=True, null=True)  # Field name made lowercase.
    compet_rate = models.TextField(db_column='COMPET_RATE', blank=True, null=True)  # Field name made lowercase.
    house_manage_no = models.BigIntegerField(db_column='HOUSE_MANAGE_NO', primary_key=True)  # Field name made lowercase.
    model_no = models.TextField(db_column='MODEL_NO', blank=True, null=True)  # Field name made lowercase.
    top_score = models.BigIntegerField(db_column='TOP_SCORE', blank=True, null=True)  # Field name made lowercase.
    total_req = models.TextField(db_column='TOTAL_REQ', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'competition'


class Detail(models.Model):
    address = models.TextField(db_column='ADDRESS', blank=True, null=True)  # Field name made lowercase.
    build_comp = models.TextField(db_column='BUILD_COMP', blank=True, null=True)  # Field name made lowercase.
    house_manage_no = models.BigIntegerField(db_column='HOUSE_MANAGE_NO', primary_key=True)  # Field name made lowercase.
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
    supply_size = models.BigIntegerField(db_column='SUPPLY_SIZE', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'detail'

class Convinient(models.Model):
    id = models.BigIntegerField(primary_key=True)
    lat = models.TextField(blank=True, null=True)
    lot = models.TextField(blank=True, null=True)
    place = models.TextField(blank=True, null=True)
    sname = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'convinient'

class Hospital(models.Model):
    dutyeryn_code = models.TextField(db_column='dutyEryn_code', blank=True, null=True)  # Field name made lowercase.
    duty_emcls_code = models.TextField(db_column='duty_Emcls_code', blank=True, null=True)  # Field name made lowercase.
    duty_code = models.TextField(blank=True, null=True)
    hname = models.TextField(blank=True, null=True)
    id = models.BigIntegerField(primary_key=True)
    lat = models.TextField(blank=True, null=True)
    lot = models.TextField(blank=True, null=True)
    place = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'hospital'


class Infra(models.Model):
    house_manage_no = models.BigIntegerField(db_column='HOUSE_MANAGE_NO', primary_key=True)  # Field name made lowercase.
    school = models.TextField(blank=True, null=True)
    subway = models.TextField(blank=True, null=True)
    mart = models.TextField(blank=True, null=True)
    park = models.TextField(blank=True, null=True)
    hospital = models.TextField(blank=True, null=True)
    busstop = models.TextField(db_column='busStop', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'infra'


class Mart(models.Model):
    id = models.BigIntegerField(primary_key=True)
    lat = models.TextField(blank=True, null=True)
    lot = models.TextField(blank=True, null=True)
    mart_name = models.TextField(blank=True, null=True)
    start_date = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mart'


class Park(models.Model):
    id = models.BigIntegerField(primary_key=True)
    lat = models.TextField(blank=True, null=True)
    lot = models.TextField(blank=True, null=True)
    park_name = models.TextField(blank=True, null=True)
    park_type = models.TextField(blank=True, null=True)
    place = models.TextField(blank=True, null=True)
    start_date = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'park'


class School(models.Model):
    id = models.BigIntegerField(primary_key=True)
    lat = models.TextField(blank=True, null=True)
    lot = models.TextField(blank=True, null=True)
    place = models.TextField(blank=True, null=True)
    school_kind = models.TextField(blank=True, null=True)
    school_name = models.TextField(blank=True, null=True)
    start_date = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'school'


class SoldCostMean(models.Model):
    place_code = models.TextField(primary_key=True)
    area_grade = models.TextField(blank=True, null=True)
    month = models.TextField(blank=True, null=True)
    mean_cost = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sold_cost_mean'


class Subway(models.Model):
    id = models.BigIntegerField(primary_key=True)
    lat = models.FloatField(blank=True, null=True)
    lot = models.FloatField(blank=True, null=True)
    place = models.TextField(blank=True, null=True)
    route_name = models.TextField(blank=True, null=True)
    stn_name = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'subway'
