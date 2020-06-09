-- Reference data for ENE database

-- (Ref *1) Regions of the base of 16 regions including Ñuble
create table ene_region (
	id tinyint(1) unsigned primary key not null,
    region_name varchar(100),
    region_name_es varchar(100)
);

-- (Ref *2) Regions of the base of 15 regions not including Ñuble
create table ene_region_15 (
	id tinyint(1) unsigned primary key not null,
    region_15_name varchar(100),
    region_15_name_es varchar(100)
);

-- (Ref *3) Geographical stratum codes based on commune + urban/rural location
create table ene_estrato (
	id smallint(2) unsigned primary key not null,
    estrato_name varchar(100),
    estrato_name_es varchar(100)
);

-- (Ref *4) Geographical stratum codes for 15 regions
create table ene_estrato_15 (
	id smallint(2) unsigned primary key not null,
    estrato_15_name varchar(100),
    estrato_15_name_es varchar(100)
);

-- (Ref *5) Stratum type
create table ene_tipo (
	id tinyint(1) unsigned primary key not null,
    abbr varchar(100),
    tipo_name varchar(100),
    tipo_name_es varchar(100)
);

-- (Ref *6) Commune code assigned by Regional Development Subsecretary
create table ene_r_p_c (
	id int(4) unsigned primary key not null,
    r_p_c_name varchar(100),
    r_p_c_name_es varchar(100)
);

-- (Ref *7) Commune code for 15 regions
create table ene_r_p_c_15 (
	id int(4) unsigned primary key not null,
    r_p_c_15_name varchar(100),
    r_p_c_15_name_es varchar(100)
);

-- (Ref *8) Sex
create table ene_sexo (
	id tinyint(1) unsigned primary key not null,
    sexo_name varchar(100),
    sexo_name_es varchar(100)
);

-- (Ref *9) Relationship to the head of household
create table ene_parentesco (
	id tinyint(1) unsigned primary key not null,
    parentesco_name varchar(100),
    parentesco_name_es varchar(100)
);

-- (Ref *10) Education level
create table ene_nivel (
	id smallint(2) unsigned primary key not null,
    nivel_name varchar(100),
    nivel_name_es varchar(100)
);

-- (Ref *11) Marital status
create table ene_est_conyugal (
	id tinyint(1) unsigned primary key not null,
    est_conyugal_name varchar(100),
    est_conyugal_name_es varchar(100)
);

-- (Ref *12) Nationality
create table ene_nacionalidad (
	id smallint(2) unsigned primary key not null,
    nacionalidad_name varchar(100),
    nacionalidad_name_es varchar(100)
);

-- (Ref *13) Reason of not working
create table ene_a6 (
	id tinyint(1) unsigned primary key not null,
    a6_reason_name varchar(100),
    a6_reason_name_es varchar(100)
);

-- (Ref *14)
create table ene_a8 (
	id tinyint(1) unsigned primary key not null,
    a8_return_period varchar(100),
    a8_return_period_es varchar(100)
);

-- (Ref *15) Occupation group according to CIUO - 08 (refers to 2 columns in ENE)
create table ene_occupation (
	id tinyint(1) unsigned primary key not null,
    occupation_name varchar(100),
    occupation_name_es varchar(100)
)

-- (Ref *16) Occupation type
create table ene_b2 (
	id tinyint(1) unsigned primary key not null,
    b2_occupation_type varchar(200),
    b2_occupation_type_es varchar(200)
)

-- (Ref *17) Compensation type
create table ene_b3 (
	id tinyint(1) unsigned primary key not null,
    b3_compensation_type varchar(100),
    b3_compensation_type_es varchar(100)
)

-- (Ref *18) Employer type
create table ene_b5 (
	id tinyint(1) unsigned primary key not null,
    b5_employer_type varchar(100),
    b5_employer_type_es varchar(100)
)

-- (Ref *19) Work type in private home
create table ene_b6 (
	id tinyint(1) unsigned primary key not null,
    b6_work_type varchar(100),
    b6_work_type_es varchar(100)
)

-- (Ref *20) Contract type (full time/part time)
create table ene_b9 (
	id tinyint(1) unsigned primary key not null,
    b9_contract_type varchar(100),
    b6_contract_type_es varchar(100)
)

-- (Ref *21) Season contract term reason
create table ene_b10 (
	id tinyint(1) unsigned primary key not null,
    b10_contract_term_reason varchar(100),
    b10_contract_term_reason_es varchar(100)
)

-- (Ref *22) Payment conditions
create table ene_b11 (
	id tinyint(1) unsigned primary key not null,
    b11_payment_conditions varchar(100),
    b11_payment_conditions_es varchar(100)
)

-- (Ref *23) Contractor type
create table ene_b12 (
	id tinyint(1) unsigned primary key not null,
    b12_contractor_type varchar(100),
    b12_contractor_type_es varchar(100)
)

-- (Ref *24) Economic activity codes used up to 2016-11
create table ene_economic_activity (
	id smaillint(2) unsigned primary key not null,
    economic_activity_name varchar(150),
    economic_activity_name_es varchar(150)
)

-- (Ref *25) Economic activity codes used from to 2016-11
create table ene_economic_activity_caenes (
	id tinyint(1) unsigned primary key not null,
    caenes_name varchar(150),
    caenes_name_es varchar(150)
)

-- (Ref *26) Number of employees
create table ene_b15_1 (
	id tinyint(1) unsigned primary key not null,
    b15_1_number_of_employees varchar(100),
    b15_1_number_of_employees_es varchar(100)
);

-- (Ref *27) Workplace location
create table ene_b16 (
	id tinyint(1) unsigned primary key not null,
    b16_workplace_location_name varchar(100),
    b16_workplace_location_name_es varchar(100)
);

-- (Ref *28) Employer registration in SII
create table ene_i1 (
	id tinyint(1) unsigned primary key not null,
    i1_employer_registration varchar(100),
    i1_employer_registration_es varchar(100)
);

-- (Ref *29) Employer business name
create table ene_i3 (
	id tinyint(1) unsigned primary key not null,
    i3_employer_business_name varchar(100),
    i3_employer_business_name_es varchar(100)
);

-- (Ref *30) Employer type
create table ene_i5 (
	id tinyint(1) unsigned primary key not null,
    i5_employer_type varchar(100),
    i5_employer_type_es varchar(100)
);

-- (Ref *31) Employer accounting
create table ene_i6 (
	id tinyint(1) unsigned primary key not null,
    i6_employer_accounting varchar(100),
    i6_employer_accounting_es varchar(100)
);

-- (Ref *32) Reason to work different number of hours
create table ene_c9 (
	id tinyint(1) unsigned primary key not null,
    c9_different_hours_reason varchar(100),
    c9_different_hours_reason_es varchar(100)
);

-- (Ref *33) Availability for extra hours
create table ene_c11 (
	id tinyint(1) unsigned primary key not null,
    c11_availability_extra_hours varchar(100),
    c11_availability_extra_hours_es varchar(100)
);

-- (Ref *34) Reason why not working extra hours
create table ene_c12 (
	id tinyint(1) unsigned primary key not null,
    c12_reason_no_extra_hours varchar(100),
    c12_reason_no_extra_hours_es varchar(100)
);

-- (Ref *35) Reason to look for a new job
create table ene_e4 (
	id tinyint(1) unsigned primary key not null,
    e4_reason_look_for_new_job varchar(100),
    e4_reason_look_for_new_job_es varchar(100)
);

-- (Ref *36) Last time looking for a job
create table ene_e5 (
	id tinyint(1) unsigned primary key not null,
    e5_job_search_last_time varchar(100),
    e5_job_search_last_time_es varchar(100)
);

-- (Ref *37) Desired employment type
create table ene_work_day (
	id tinyint(1) unsigned primary key not null,
    work_day_type varchar(100),
    work_day_type_es varchar(100)
);

-- (Ref *38) Desired contract type
create table ene_e8 (
	id tinyint(1) unsigned primary key not null,
    e8_desired_contract_type varchar(100),
    e8_desired_contract_type_es varchar(100)
);

-- (Ref *39) Reason not to look for a job
create table ene_e9 (
	id tinyint(1) unsigned primary key not null,
    e9_no_looking_reason_name varchar(100),
    e9_no_looking_reason_name_es varchar(100)
);

-- (Ref *40) Reason not to be available for a new job
create table ene_e12 (
	id tinyint(1) unsigned primary key not null,
    e12_not_available_reason_name varchar(100),
    e12_not_available_reason_name_es varchar(100)
);

-- (Ref *41) Employment role / Occupation category
create table ene_categoria_ocupacion (
	id tinyint(1) unsigned primary key not null,
    categoria_ocupacion_name varchar(100),
    categoria_ocupacion_name_es varchar(100)
);

-- (Ref *42) Reason to leave
create table ene_e19 (
	id tinyint(1) unsigned primary key not null,
    e19_leave_reason_name varchar(150),
    e19_leave_reason_name_es varchar(150)
);

-- (Ref *43) General condition of economic activity
create table ene_cae_general (
	id tinyint(1) unsigned primary key not null,
    cae_general_name varchar(100),
    cae_general_name_es varchar(100)
);

-- (Ref *44) Specific condition of economic activity
create table ene_cae_especifico (
	id tinyint(1) unsigned primary key not null,
    cae_especifico_name varchar(100),
    cae_especifico_name_es varchar(100)
);

-- (Ref *45) Education level (international classification)
create table ene_cine (
	id smallint(2) unsigned primary key not null,
    cine_name varchar(100),
    cine_name_es varchar(100)
);

-- (Ref *46) Employment sector
create table ene_sector (
	id tinyint(1) unsigned primary key not null,
    sector_name varchar(100),
    sector_name_es varchar(100)
);

-- (Ref *47) Activity condition
create table ene_ocup_form (
	id tinyint(1) unsigned primary key not null,
    ocup_form_name varchar(100),
    ocup_form_name_es varchar(100)
);

-- (Ref *48) Activity condition
create table ene_activ (
	id tinyint(1) unsigned primary key not null,
    activ_name varchar(100),
    activ_name_es varchar(100)
);

-- (Ref *49) YES-NO standard answers
create table ene_yes_no (
	id tinyint(1) unsigned primary key not null,
    yes_no_std varchar(50),
    yes_no_std_es varchar(50)
)
