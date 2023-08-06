# Changelog

<!--next-version-placeholder-->

## v9.3.5 (2022-05-04)
### Fix
* Add document_id to visa serializer ([`2ec598a`](https://github.com/bimdata/python-api-client/commit/2ec598a2b1bdc0ebdf270e7c74df463327a2db28))

## v9.3.4 (2022-05-04)
### Fix
* Visa serialization in document (#522)

* visa serialization in document

* no prefetch tag ([`213c4d7`](https://github.com/bimdata/python-api-client/commit/213c4d7141e9c5c8fc00d80e21739d1dfa2f8bf8))

## v9.3.3 (2022-05-03)
### Fix
* Reorder document history ([`c1afe9e`](https://github.com/bimdata/python-api-client/commit/c1afe9ea010a61da0ed2d0c0c7e43437e56bd311))

## v9.3.2 (2022-05-02)
### Fix
* Serialize document creator ([`cb1f35c`](https://github.com/bimdata/python-api-client/commit/cb1f35c2348a89acb7f8f0b3d47ff5d86e4eb80b))

## v9.3.1 (2022-04-29)
### Fix
* Remove parent from document serialization ([#521](https://github.com/bimdata/python-api-client/issues/521)) ([`fbc5445`](https://github.com/bimdata/python-api-client/commit/fbc544512b74cc852b2b6f155cb2b62b79122289))

## v9.3.0 (2022-04-29)
### Feature
* Feat/versionning (#517)

* add model, migrations, views, serializers

* test DocumentHistory view

* fix last tests

* filter list model

* fix migration and add reverse_code

* renaming old_version_id ([`d562d95`](https://github.com/bimdata/python-api-client/commit/d562d9583f76b61f0f6ddf97ec80150a6fd6b902))

## v9.2.0 (2022-04-21)
### Feature
* Add bcf pins (#515)

* add bcf pins

* add view tests ([`8948499`](https://github.com/bimdata/python-api-client/commit/8948499b4f427735081404a23b9c68fe2f1b12d4))

## v9.1.1 (2022-04-20)
### Fix
* Fix createDocument response missing ([`a7a4208`](https://github.com/bimdata/python-api-client/commit/a7a4208fa4163eb55e82628a570e743e217b85c3))

## v9.1.0 (2022-04-15)
### Feature
* Create document tag views (#513)

* create document tag views

* fix: serializer readOnly

* add admin tags

* add inline Tag Project ([`3c00f75`](https://github.com/bimdata/python-api-client/commit/3c00f752a14f58a4fc38ed9a3ff03ba54e005580))

## v9.0.0 (2022-04-12)
### Fix
* Fix swagger generation ([`3952685`](https://github.com/bimdata/python-api-client/commit/3952685f9c92059b94605b178693de95cd670f1d))

### Breaking
* Feat/openapi3 (#508)

* install and pre configure drf-spectacular

* finish replace drf-yasg lib by drf-spectacular

* fix error on lib generation

* recreate data for oauth delete tests

* fix some typo

* fix null enums

* fix some serializer

* add bearer auth to swagger

* add test operationId and fix numquery MPApp test

* fix head action in test doc

Co-authored-by: Amoki <hugo@bimdata.io> ([`57074b7`](https://github.com/bimdata/python-api-client/commit/57074b73f37e92e1ee0b37cdfde59b3ccd7bdd80))
* Feat/openapi3 (#508)

* install and pre configure drf-spectacular

* finish replace drf-yasg lib by drf-spectacular

* fix error on lib generation

* recreate data for oauth delete tests

* fix some typo

* fix null enums

* fix some serializer

* add bearer auth to swagger

* add test operationId and fix numquery MPApp test

* fix head action in test doc

Co-authored-by: Amoki <hugo@bimdata.io> ([`57074b7`](https://github.com/bimdata/python-api-client/commit/57074b73f37e92e1ee0b37cdfde59b3ccd7bdd80))

## v8.0.0 (2022-04-12)
### Breaking
* Feat/openapi3 (#508)

* install and pre configure drf-spectacular

* finish replace drf-yasg lib by drf-spectacular

* fix error on lib generation

* recreate data for oauth delete tests

* fix some typo

* fix null enums

* fix some serializer

* add bearer auth to swagger

* add test operationId and fix numquery MPApp test

* fix head action in test doc

Co-authored-by: Amoki <hugo@bimdata.io> ([`18591ec`](https://github.com/bimdata/python-api-client/commit/18591ec7c8156e00549d7d604500a0773b79463a))
* Feat/openapi3 (#508)

* install and pre configure drf-spectacular

* finish replace drf-yasg lib by drf-spectacular

* fix error on lib generation

* recreate data for oauth delete tests

* fix some typo

* fix null enums

* fix some serializer

* add bearer auth to swagger

* add test operationId and fix numquery MPApp test

* fix head action in test doc

Co-authored-by: Amoki <hugo@bimdata.io> ([`18591ec`](https://github.com/bimdata/python-api-client/commit/18591ec7c8156e00549d7d604500a0773b79463a))

## v7.4.2 (2022-03-17)
### Fix
* Remove comment visa nested ([#502](https://github.com/bimdata/python-api-client/issues/502)) ([`a516af8`](https://github.com/bimdata/python-api-client/commit/a516af86ac3aa3ef6858f1b75c7f36e182bf7c45))

## v7.4.1 (2022-02-25)
### Fix
* Fix create building and storey doc serializer ([`03903e7`](https://github.com/bimdata/python-api-client/commit/03903e7c077a08434ad587401dc691c5e2c8b646))

## v7.4.0 (2022-02-25)
### Feature
* Order plans in storey (#495)

* init refacto storey

* add building test

* fix serializers

* replace Counter

* init refacto storey

* order plans in storey

* merge migration ifc/88_

* fix bad merge

* fix bad merge ([`ea3cf1d`](https://github.com/bimdata/python-api-client/commit/ea3cf1d3fc82b9baa09a5536cde76e1f2cfcfc9c))

## v7.3.0 (2022-02-25)
### Feature
* Refacto storeys and add buildings (#494)

* init refacto storey

* add building test

* fix serializers

* replace Counter ([`06a735c`](https://github.com/bimdata/python-api-client/commit/06a735c75412fdfb301f7e10ecb29a5e4275afe7))

## v7.2.0 (2022-02-24)
### Feature
* Add size_ratio fields ([`2a5d90c`](https://github.com/bimdata/python-api-client/commit/2a5d90c51c5de429d10d6cf1f4d5da9da5448093))

## v7.1.2 (2022-02-24)
### Fix
* Bcf detailed extensions labels ([`7d5ade7`](https://github.com/bimdata/python-api-client/commit/7d5ade750437b1e5007c4434fdaabfd1c54d9dc9))

## v7.1.1 (2022-02-23)
### Fix
* Add creadted_at and upated_at to Propertie et PropertySet ([`9218cd7`](https://github.com/bimdata/python-api-client/commit/9218cd7ae22192003e0e09017565940604bff67c))

## v7.1.0 (2022-02-15)
### Feature
* Feature/bcf colors (#485)

* wip

* update project extensions GET method

* cleanup

* fix project extensions

* implement extension update

* add color to all existing topics

* respond with 400 if duplicated name

* remove useless config ([`64b5792`](https://github.com/bimdata/python-api-client/commit/64b579260b41558e0c959ba65dcbfe159d57fcf0))

## v7.0.1 (2022-02-15)
### Fix
* Rename last ifc operations ([#489](https://github.com/bimdata/python-api-client/issues/489)) ([`6a0bce1`](https://github.com/bimdata/python-api-client/commit/6a0bce138e8adad44c462cec339d523fc33cc346))

## v7.0.0 (2022-02-04)
### Breaking
* Rename ifc to model (#477)

* filter storey models with permissions

* duplicate ifc routes and update tags ViewSet

* add deprecated ifc views and filter by type

* rename ifc operations

* rename Ifc table

* rename some Ifc classes

* duplicate ifc test and change reverse url name

* update foreignkeys

* rename ifc_pk in model_pk

* update route name

* update scopes

* fix swagger dupplicate

* fix test projectAccessToken

* actually send keycloak scope create

* restore ifc_guid

* don't unzip unzipped structure files

* fix bad rebase ([`6d48496`](https://github.com/bimdata/python-api-client/commit/6d48496db3d7b9f80e1ffcfe407873046383e516))
* rename ifc to model (#477)

* filter storey models with permissions

* duplicate ifc routes and update tags ViewSet

* add deprecated ifc views and filter by type

* rename ifc operations

* rename Ifc table

* rename some Ifc classes

* duplicate ifc test and change reverse url name

* update foreignkeys

* rename ifc_pk in model_pk

* update route name

* update scopes

* fix swagger dupplicate

* fix test projectAccessToken

* actually send keycloak scope create

* restore ifc_guid

* don't unzip unzipped structure files

* fix bad rebase ([`6d48496`](https://github.com/bimdata/python-api-client/commit/6d48496db3d7b9f80e1ffcfe407873046383e516))

## v6.0.0 (2022-02-04)
### Breaking
* Sync with js libs ([`eb430f5`](https://github.com/bimdata/python-api-client/commit/eb430f5f2a77313a510db067276c7fe520c28adc))
* sync with js libs ([`eb430f5`](https://github.com/bimdata/python-api-client/commit/eb430f5f2a77313a510db067276c7fe520c28adc))

## v5.22.0 (2022-01-31)
### Feature
* 2d positioning (#471)

* filter storey models with permissions

* rework storey serializer

* add positioning plan to m2m (storey-plan)

* add route with params id and positioning route renaming

* include positioning in storey serializer

* fix tests ([`f8bf0c8`](https://github.com/bimdata/python-api-client/commit/f8bf0c8b641cb613d99d7a116ecd8377fab46245))

## v5.21.1 (2022-01-31)
### Fix
* Filter storey models with permissions and add models_unreachable_count field (#470)

* filter storey models with permissions

* fix test add model to storey

* rework storey serializer ([`b68c55a`](https://github.com/bimdata/python-api-client/commit/b68c55a4665fda225fd205dac533f64d9dca9ee8))

## v5.21.0 (2022-01-31)
### Feature
* Add img_format=url in BCF routes ([#472](https://github.com/bimdata/python-api-client/issues/472)) ([`9cef689`](https://github.com/bimdata/python-api-client/commit/9cef6891bd435d25098035e413489bb6735515c2))

## v5.20.1 (2022-01-28)
### Fix
* One storey site by building (#469)

* one storey site by building

* add db unique constraint

* Update ifc/v1/views.py

Co-authored-by: Hugo Duroux <hugo@bimdata.io>

* Update ifc/v1/views.py

Co-authored-by: Hugo Duroux <hugo@bimdata.io>

Co-authored-by: Hugo Duroux <hugo@bimdata.io> ([`7c907c8`](https://github.com/bimdata/python-api-client/commit/7c907c80cb76328f174e414efb73850ca81dc188))

## v5.20.0 (2022-01-27)
### Feature
* Plans and storeys (#468)

* create storey

* add migrations and route manage model children

* create metabuilding and relation between storey and model-plans

* fix signal test

* PR review

* models can update name ([`6a125d1`](https://github.com/bimdata/python-api-client/commit/6a125d1eebe97eacd063a6ef2001c9057ac57cb2))

## v5.19.1 (2022-01-18)
### Fix
* Add non automatic models (#464)

* Add non automatic models

* improve tests

* rename route and add permissions

* add model delete with doc ([`b224801`](https://github.com/bimdata/python-api-client/commit/b2248010f7890245d90e9b4f067e4ca96ea00a63))

## v5.19.0 (2022-01-14)
### Feature
* Feature/smart files (#463)

* allow many model types

* add tests

* fix document name

* more cleanup

* update ci poetry version

* do not reprocess on file update

* fix export,merge and optimize queues

* add types.py

* more contants ([`a5ba918`](https://github.com/bimdata/python-api-client/commit/a5ba9187333e0a1b754b49755322102085adacc3))

## v5.18.3 (2022-01-11)
### Fix
* (visa) add validations_in_error to serializer ([`e4df33f`](https://github.com/bimdata/python-api-client/commit/e4df33ffcaf01b3f60f7e214a2a64809d2befcf3))

## v5.18.2 (2022-01-04)
### Fix
* Fix document elements list uuids ([`39de959`](https://github.com/bimdata/python-api-client/commit/39de959c2a58e9ab3b5949542efe76456cd8cad9))

## v5.18.1 (2021-12-22)
### Fix
* Rename element_ids to element_uuids ([`461e3db`](https://github.com/bimdata/python-api-client/commit/461e3db667d2edba71b1596d694185f61d3233b5))

## v5.18.0 (2021-12-22)
### Feature
* Add element/documents route ([`68a02e7`](https://github.com/bimdata/python-api-client/commit/68a02e7d227d78ef2e4efd9bdfbe82b1b686cf89))

## v5.17.1 (2021-12-13)
### Fix
* Add document to visa serializer ([#458](https://github.com/bimdata/python-api-client/issues/458)) ([`7504aee`](https://github.com/bimdata/python-api-client/commit/7504aee678ed033bcbe517ab9fcfe7c54776bfcf))

## v5.17.0 (2021-12-09)
### Feature
* Feature/link element document (#457)

* add documents to elements

* add test for filterred ifc and document list

* typo

* add some query optimizations ([`92814d1`](https://github.com/bimdata/python-api-client/commit/92814d193cd97e2feddbed979806ed702db7301d))

## v5.16.0 (2021-12-06)
### Feature
* Feature/visa (#451)

* add invitation to userProject

* PR changes requests

* init visa

* fix: boolean swagger bad import

* fix: git conflict migrations, replace tests 'put'

* add visa project view and change perform_created method on others views

* fix: duplicate swagger operation id on getComment*

* review PR and add permission mixin actions

* fix tests

* fix swagger

* add nested mixin to self visa project view

* fix creator filter view

* print test

* bypass schrodinger swagger pb

* clean useless db requests in permissions

* restore 404 ifc tests

* add userproject to serializers context ([`a963e5f`](https://github.com/bimdata/python-api-client/commit/a963e5f94af8f3e4d098856adc9253a0cb473252))

## v5.15.2 (2021-12-02)
### Fix
* Add id to Public Organization Serializer ([`5ac3574`](https://github.com/bimdata/python-api-client/commit/5ac357430084e206b40537112334d8de4075f805))

## v5.15.1 (2021-12-02)
### Fix
* Add organization serializer in App and MPApp serializers (#452)

* add organization serializer in App and MPApp serializers

* fix test and add select related

* use Public Organization Serializer ([`b1f0958`](https://github.com/bimdata/python-api-client/commit/b1f0958e511655ca19ddbf52ab35fbb1d1fd1fc2))

## v5.15.0 (2021-11-24)
### Feature
* Remove deprecated and put (#450)

* remove deprecated route and PUT route without BCF routes

* fix some tests

* fix last tests and restore project tree route

* restore BCF tests change

* rename fullUpdate operation ([`5769df5`](https://github.com/bimdata/python-api-client/commit/5769df5195f22e65696b4c46ed1a8ee925634526))
* Add leave project route (#449)

* Add leave project route

* fix roles ([`4d52c51`](https://github.com/bimdata/python-api-client/commit/4d52c51628bf3e977074dfec3d8af51615a13c2d))

### Fix
* Fix semantic release ([`aca3560`](https://github.com/bimdata/python-api-client/commit/aca3560c5d69a91d32be6992c0d8aea1153110b4))
* Fix serializer user project (#448)

Breaking Change:
 -  key to  for GroupUser create view
 - Route pk for userProject views is now UserProject pk and not FosUser pk

Some other change:
- fix serializer of userProject for swagger and libs
- add missing invitation user project from project and group
- fix some test ([`8b5446a`](https://github.com/bimdata/python-api-client/commit/8b5446a58252f767665f6cd3fff59af93baddfbd))
* Add invitation key in UserProject ([`30a8fb5`](https://github.com/bimdata/python-api-client/commit/30a8fb5ad88a6aed47de4bcb69a34cd37702e5ff))
* Get cloud size operation id in openapi ([`d508862`](https://github.com/bimdata/python-api-client/commit/d5088627492eec9d1ea02a8915cfb1d7ed4ce09c))
* Fix list/create methods openAPI ([`7519d93`](https://github.com/bimdata/python-api-client/commit/7519d931205caffc57f964e92e0547714d916304))

## v5.14.0 (2021-09-13)
### Feature
* Serialize user-permissions on documents ([`8597421`](https://github.com/bimdata/python-api-client/commit/859742176f6e0827c170dd8d30c95c254d502fcc))
* Add profile_picture field in user serialization

* add user picture field

* fix user.company, add comment about an edge case ([`45bd37c`](https://github.com/bimdata/python-api-client/commit/45bd37ce3e9ead5bb4050fa2a26a609a64e8ac26))
* Add GED permissions ([`00b987a`](https://github.com/bimdata/python-api-client/commit/00b987af3d7f310c07beb9d30c7354b9e5830d26))
* Allow bigger guids ([#420](https://github.com/bimdata/python-api-client/issues/420)) ([`54b2b09`](https://github.com/bimdata/python-api-client/commit/54b2b090cbbf127cf8ac0f17c3492e6d0e1c7f29))

### Fix
* Allow empty name in raw layers and raw materials ([`b96d9a7`](https://github.com/bimdata/python-api-client/commit/b96d9a7eb1e3828fd2b3f7e9edb558b296d38f0b))
* Allow empty name in raw layers and raw materials ([`c0d6bb6`](https://github.com/bimdata/python-api-client/commit/c0d6bb6f662d3289915da48580553bb2277c7ee7))
* Allow empty name in raw layers and raw materials ([`22e450d`](https://github.com/bimdata/python-api-client/commit/22e450d38322621610ca85750524c94dd197f33c))
* Fix dms-tree group permissions ([`38f8ce5`](https://github.com/bimdata/python-api-client/commit/38f8ce5608ad11f8dd1518a9a901da5ef8779bdd))
* Fix field name and add field to children dms-tree ([#426](https://github.com/bimdata/python-api-client/issues/426)) ([`2881af8`](https://github.com/bimdata/python-api-client/commit/2881af81fb7ae5fe2718f8187ffc5ae350aa4ebd))
