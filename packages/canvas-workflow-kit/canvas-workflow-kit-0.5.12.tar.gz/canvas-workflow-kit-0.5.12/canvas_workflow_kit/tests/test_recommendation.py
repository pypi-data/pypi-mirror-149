from canvas_workflow_kit.intervention import Intervention
from canvas_workflow_kit.patient import Patient
from canvas_workflow_kit.recommendation import (
    AllergyRecommendation,
    DiagnoseRecommendation,
    FollowUpRecommendation,
    HyperlinkRecommendation,
    ImagingRecommendation,
    ImmunizationRecommendation,
    InstructionRecommendation,
    InterviewRecommendation,
    LabRecommendation,
    PlanRecommendation,
    PrescribeRecommendation,
    Recommendation,
    ReferRecommendation,
    TaskRecommendation,
    VitalSignRecommendation
)
from canvas_workflow_kit.value_set.v2018 import (
    AboveNormalFollowUp,
    CtColonography,
    Diabetes,
    FitDna,
    Hba1CLaboratoryTest,
    InfluenzaVaccine_1254,
    LimitedLifeExpectancy,
    TobaccoUseCessationPharmacotherapy,
    TobaccoUseScreening
)
from canvas_workflow_kit.value_set.value_set import ValueSet

from .base import SDKBaseTest


class RecommendationTest(SDKBaseTest):

    def test___init__(self):
        rec = Recommendation(
            key='KEY-ID',
            rank=123,
            button='ACT',
            title='Do Something',
            narrative="I'm not sure what, but do something!")
        self.assertTrue(isinstance(rec, Recommendation))
        self.assertEqual(rec.title, 'Do Something')
        self.assertEqual(rec.narrative, "I'm not sure what, but do something!")
        self.assertEqual(rec.command, {})
        self.assertEqual(rec.key, 'KEY-ID')
        self.assertEqual(rec.rank, 123)
        self.assertEqual(rec.button, 'ACT')

    def test_command_filter(self):
        rec = Recommendation(
            key='KEY-ID', rank=123, button='ACT', title='Something', narrative='Do something!')

        class UnitTestReco1(ValueSet):
            OID = '1.2.3.4'
            VALUE_SET_NAME = 'Reco A for the unit tests'
            CPT = {'abc', '123'}
            SNOMEDCT = {'12345', '23456', '34567'}

        class UnitTestReco2(ValueSet):
            OID = '5.2.3.4'
            VALUE_SET_NAME = 'Reco B for the unit tests'
            CPT = {'xbc', '423'}
            SNOMEDCT = {'612345', '73456', '84567'}

        expected = {
            'type': 'atype',
            'filter': {
                'coding': [{
                    'system': 'cpt',
                    'code': ['123', 'abc', 'xbc', '423']
                }, {
                    'system': 'snomedct',
                    'code': ['34567', '12345', '23456', '612345', '73456', '84567']
                }]
            }
        }  # yapf: disable
        result = rec.command_filter('atype', [UnitTestReco1, UnitTestReco2])
        HelperCommand().equal_commands(expected, result)


class AllergyRecommendationTest(SDKBaseTest):
    def test__init__(self):
        class AllergyTestValueSet(ValueSet):
            VALUE_SET_NAME = 'Enterococcus faecalis'
            FDB = {'1226'}

        rec = AllergyRecommendation(
            key='ALLERGY', rank=1, button='Allergy', allergy=AllergyTestValueSet,
            narrative='rash and hives', context={'severity': 'mild', 'onset_date': '2020-01-01'})
        self.assertIsInstance(rec, Recommendation)
        self.assertEqual(rec.key, 'ALLERGY')
        self.assertEqual(rec.rank, 1)
        self.assertEqual(rec.button, 'Allergy')
        self.assertEqual(rec.title, 'Enterococcus faecalis')
        self.assertEqual(rec.narrative, 'rash and hives')
        self.assertEqual(rec.context['severity'], 'mild')
        self.assertEqual(rec.context['onset_date'], '2020-01-01')

        expected = {
            'type': 'allergy',
            'filter': {
                'coding': [{
                    'system': 'fdb',
                    'code': ['1226']
                }]
            }
        }
        result = rec.command
        HelperCommand().equal_commands(expected, result)


class DiagnoseRecommendationTest(SDKBaseTest):
    def test__init__(self):
        patient = self.load_patient('full')
        self.assertIsInstance(patient, Patient)

        class DiagnoseTestValueSet(ValueSet):
            VALUE_SET_NAME = 'Senile purpura'
            ICD10CM = {'D692'}
            INTERNAL = {'PAT.QUES.8'}

        rec = DiagnoseRecommendation(
            key='DIAGNOSE', rank=1, button='Diagnose', patient=patient,
            condition=DiagnoseTestValueSet)
        self.assertIsInstance(rec, Recommendation)
        self.assertEqual(rec.key, 'DIAGNOSE')
        self.assertEqual(rec.rank, 1)
        self.assertEqual(rec.button, 'Diagnose')
        self.assertEqual(rec.title, 'Senile purpura')
        self.assertEqual(rec.narrative, 'Consider diagnosing Darey with Senile purpura')

        expected = {
            'type': 'diagnose',
            'filter': {
                'coding': [{
                    'system': 'icd10cm',
                    'code': ['D692']
                }, {
                    'system': 'internal',
                    'code': ['PAT.QUES.8']
                }]
            }
        }
        result = rec.command
        HelperCommand().equal_commands(expected, result)


class FollowUpRecommendationTest(SDKBaseTest):
    def test__init__(self):
        patient = self.load_patient('full')
        self.assertIsInstance(patient, Patient)

        rec = FollowUpRecommendation(
            key='FOLLOWUP', rank=1, button='Follow Up', patient=patient,
            title='Request follow up office visit on 3/5/22',
            context={'requested_appointment_type': 'office', 'requested_date': '2022-03-05',
                     'reason_for_visit': 'covid vaccine booster',
                     'internal_comment': 'make sure he brings his covid vaccination card'})
        self.assertIsInstance(rec, Recommendation)
        self.assertEqual(rec.key, 'FOLLOWUP')
        self.assertEqual(rec.rank, 1)
        self.assertEqual(rec.button, 'Follow Up')
        self.assertEqual(rec.title, 'Request follow up office visit on 3/5/22')
        self.assertEqual(rec.narrative, 'Darey needs a follow-up appointment')
        self.assertEqual(rec.context['requested_appointment_type'], 'office')
        self.assertEqual(rec.context['requested_date'], '2022-03-05')
        self.assertEqual(
            rec.context['internal_comment'],
            'make sure he brings his covid vaccination card')
        self.assertEqual(rec.command, {'type': 'followUp'})


class ImagingRecommendationTest(SDKBaseTest):

    def test___init__(self):
        patient = self.load_patient('full')
        self.assertIsInstance(patient, Patient)

        rec = ImagingRecommendation(
            key='KEY-ID', rank=123, button='ACT', patient=patient, imaging=CtColonography,
            context={'foo': 'bar'})
        self.assertIsInstance(rec, Recommendation)
        self.assertEqual(rec.key, 'KEY-ID')
        self.assertEqual(rec.rank, 123)
        self.assertEqual(rec.button, 'ACT')

        expected = 'Darey should be ordered CT Colonography.'
        self.assertEqual(expected, rec.narrative)

        expected = 'Order CT Colonography'
        self.assertEqual(expected, rec.title)

        self.assertEqual(rec.context['foo'], 'bar')

        expected = {
            'type': 'imagingOrder',
            'filter': {
                'coding': [{
                    'system': 'cpt',
                    'code': ['74263']
                }, {
                    'system': 'snomedct',
                    'code': ['418714002']
                }]
            }
        }
        result = rec.command
        HelperCommand().equal_commands(expected, result)


class ReferRecommendationTest(SDKBaseTest):

    def test___init__(self):
        patient = self.load_patient('full')
        self.assertIsInstance(patient, Patient)

        rec = ReferRecommendation(key='KEY-ID', rank=123, button='ACT',
                                  patient=patient, referral=FitDna, context={'foo': 'bar'})
        self.assertIsInstance(rec, Recommendation)
        self.assertEqual(rec.key, 'KEY-ID')
        self.assertEqual(rec.rank, 123)
        self.assertEqual(rec.button, 'ACT')

        expected = 'Darey should be referred for FIT DNA.'
        self.assertEqual(expected, rec.narrative)

        expected = 'Refer FIT DNA'
        self.assertEqual(expected, rec.title)

        self.assertEqual(rec.context['foo'], 'bar')

        expected = {
            'type': 'refer',
            'filter': {
                'coding': [{
                    'system': 'loinc',
                    'code': ['77354-9', '77353-1']
                }]
            }
        }
        result = rec.command
        HelperCommand().equal_commands(expected, result)


class LabRecommendationTest(SDKBaseTest):

    def test___init__(self):
        patient = self.load_patient('full')
        self.assertIsInstance(patient, Patient)

        rec = LabRecommendation(
            key='KEY-ID',
            rank=123,
            button='ACT',
            patient=patient,
            lab=Hba1CLaboratoryTest,
            condition=Diabetes,
            context={'foo': 'bar'})
        self.assertIsInstance(rec, Recommendation)
        self.assertEqual(rec.key, 'KEY-ID')
        self.assertEqual(rec.rank, 123)
        self.assertEqual(rec.button, 'ACT')

        expected = 'Darey has Diabetes and a HbA1c Laboratory Test is recommended.'
        self.assertEqual(expected, rec.narrative)

        expected = 'Order HbA1c Laboratory Test'
        self.assertEqual(expected, rec.title)

        self.assertEqual(rec.context['foo'], 'bar')

        expected = {
            'type': 'labOrder',
            'filter': {
                'coding': [{
                    'system': 'loinc',
                    'code': ['4548-4', '17856-6', '4549-2']
                }]
            }
        }
        result = rec.command
        HelperCommand().equal_commands(expected, result)


class ImmunizationRecommendationTest(SDKBaseTest):

    def test___init__(self):
        patient = self.load_patient('full')
        self.assertIsInstance(patient, Patient)

        rec = ImmunizationRecommendation(
            key='KEY-ID',
            rank=123,
            button='ACT',
            patient=patient,
            immunization=InfluenzaVaccine_1254,
            context={'foo': 'bar'})
        self.assertIsInstance(rec, Recommendation)
        self.assertEqual(rec.key, 'KEY-ID')
        self.assertEqual(rec.rank, 123)
        self.assertEqual(rec.button, 'ACT')

        expected = 'Darey should get an Influenza Vaccine.'
        self.assertEqual(expected, rec.narrative)

        expected = 'Order Influenza Vaccine'
        self.assertEqual(expected, rec.title)

        self.assertEqual(rec.context['foo'], 'bar')

        expected = {
            'type': 'immunization',
            'filter': {
                'coding': [{
                    'system': 'cvx',
                    'code': [
                        '88', '155', '168', '171', '150', '158', '135', '144', '166', '141', '161',
                        '153', '140'
                    ]
                }]
            }
        }
        result = rec.command
        HelperCommand().equal_commands(expected, result)


class InstructionRecommendationTest(SDKBaseTest):

    def test___init__(self):
        patient = self.load_patient('full')
        self.assertIsInstance(patient, Patient)

        rec = InstructionRecommendation(
            key='KEY-ID', rank=123, button='ACT', patient=patient, instruction=AboveNormalFollowUp,
            context={'foo': 'bar'})
        self.assertIsInstance(rec, Recommendation)
        self.assertEqual(rec.key, 'KEY-ID')
        self.assertEqual(rec.rank, 123)
        self.assertEqual(rec.button, 'ACT')

        expected = 'Darey should get an Above Normal Follow-up.'
        self.assertEqual(expected, rec.narrative)

        expected = 'Instruct Above Normal Follow-up'
        self.assertEqual(expected, rec.title)

        self.assertEqual(rec.context['foo'], 'bar')

        expected = {
            'type': 'instruct',
            'filter': {
                'coding': [{
                    'system': 'cpt',
                    'code': [
                        '97804', '43888', '97802', '43774', '43772', '98960', '43845', '43842',
                        '99401', '43843', '43644', '43846', '43770', '43773', '97803', '43659',
                        '43645', '43847', '99402', '43771', '43886', '99078', '43848'
                    ]
                }, {
                    'system': 'hcpcs',
                    'code': [
                        'G0447', 'G0271', 'S9449', 'S9451', 'S9470', 'G0473', 'S9452', 'G0270'
                    ]
                }, {
                    'system': 'icd10cm',
                    'code': ['Z713']
                }, {
                    'system': 'snomedct',
                    'code': [
                        '386291006', '386292004', '361231003', '370847001', '413315001',
                        '304549008', '424753004', '386464006', '307818003', '386373004',
                        '386463000', '418995006', '443288003', '410177006'
                    ]
                }]
            }
        }  # yapf: disable
        result = rec.command
        HelperCommand().equal_commands(expected, result)


class InterviewRecommendationTest(SDKBaseTest):

    def test___init__(self):
        patient = self.load_patient('full')
        self.assertIsInstance(patient, Patient)

        rec = InterviewRecommendation(
            key='KEY-ID',
            rank=123,
            button='ACT',
            patient=patient,
            questionnaires=[TobaccoUseScreening, LimitedLifeExpectancy],
            context={'foo': 'bar'})
        self.assertIsInstance(rec, Recommendation)
        self.assertEqual(rec.key, 'KEY-ID')
        self.assertEqual(rec.rank, 123)
        self.assertEqual(rec.button, 'ACT')

        expected = 'Darey should be given a Tobacco Use Screening, Limited Life Expectancy.'
        self.assertEqual(expected, rec.narrative)

        expected = 'Interview Tobacco Use Screening, Limited Life Expectancy'
        self.assertEqual(expected, rec.title)

        self.assertEqual(rec.context['foo'], 'bar')

        expected = {
            'type': 'interview',
            'filter': {
                'coding': [{
                    'system': 'loinc',
                    'code': ['72166-2', '68536-2', '39240-7', '68535-4']
                }, {
                    'system': 'snomedct',
                    'code': ['300936002', '27143004', '162608008', '170969009', '162607003']
                }]
            }
        }  # yapf: disable
        result = rec.command
        HelperCommand().equal_commands(expected, result)


class PrescribeRecommendationTest(SDKBaseTest):

    def test___init__(self):
        patient = self.load_patient('full')
        self.assertIsInstance(patient, Patient)

        rec = PrescribeRecommendation(
            key='KEY-ID',
            rank=123,
            button='ACT',
            patient=patient,
            prescription=TobaccoUseCessationPharmacotherapy,
            context={'foo': 'bar'})
        self.assertIsInstance(rec, Recommendation)
        self.assertEqual(rec.key, 'KEY-ID')
        self.assertEqual(rec.rank, 123)
        self.assertEqual(rec.button, 'ACT')

        expected = 'Darey should be prescribed Tobacco Use Cessation Pharmacotherapy.'
        self.assertEqual(expected, rec.narrative)

        expected = 'Prescribe Tobacco Use Cessation Pharmacotherapy'
        self.assertEqual(expected, rec.title)

        self.assertEqual(rec.context['foo'], 'bar')

        expected = {
            'type': 'prescribe',
            'filter': {
                'coding': [{
                    'system': 'rxnorm',
                    'code': [
                        '892244', '993550', '151226', '198045', '199889', '1551468', '993691',
                        '198047', '1801289', '1232585', '317136', '998675', '993518', '993536',
                        '1797886', '993567', '198046', '359817', '998679', '993541', '993557',
                        '359818', '199283', '198029', '311975', '250983', '749788', '198030',
                        '749289', '998671', '205315', '993687', '205316', '636671', '993681',
                        '993503', '199890', '198031', '199888', '312036', '636676', '314119'
                    ]  # yapf: disable
                }]
            }
        }
        result = rec.command
        HelperCommand().equal_commands(expected, result)


class VitalSignRecommendationTest(SDKBaseTest):

    def test___init__(self):
        patient = self.load_patient('full')
        self.assertIsInstance(patient, Patient)

        rec = VitalSignRecommendation(key='KEY-ID', rank=123, button='ACT',
                                      patient=patient, context={'foo': 'bar'})
        self.assertIsInstance(rec, Recommendation)
        self.assertEqual(rec.key, 'KEY-ID')
        self.assertEqual(rec.rank, 123)
        self.assertEqual(rec.button, 'ACT')
        self.assertEqual('Darey should vital signs collected.', rec.narrative)
        self.assertEqual('Collect vitals', rec.title)
        self.assertEqual({'type': 'vitalSign'}, rec.command)
        self.assertEqual(rec.context['foo'], 'bar')


class PlanRecommendationTest(SDKBaseTest):

    def test___init__(self):
        patient = self.load_patient('full')
        self.assertIsInstance(patient, Patient)

        rec = PlanRecommendation(key='KEY-ID', rank=123, button='ACT',
                                 patient=patient, context={'foo': 'bar'})
        self.assertIsInstance(rec, Recommendation)
        self.assertEqual(rec.key, 'KEY-ID')
        self.assertEqual(rec.rank, 123)
        self.assertEqual(rec.button, 'ACT')
        self.assertEqual('Darey should have a plan.', rec.narrative)
        self.assertEqual('Make a plan', rec.title)
        self.assertEqual({'type': 'plan'}, rec.command)
        self.assertEqual(rec.context['foo'], 'bar')


class TaskRecommendationTest(SDKBaseTest):

    def test___init__(self):
        patient = self.load_patient('full')
        self.assertIsInstance(patient, Patient)

        rec = TaskRecommendation(key='KEY-ID', rank=123, title='TITLE',
                                 button='ACT', patient=patient, context={'foo': 'bar'})

        self.assertIsInstance(rec, Recommendation)
        self.assertEqual(rec.key, 'KEY-ID')
        self.assertEqual(rec.title, 'TITLE')
        self.assertEqual(rec.rank, 123)
        self.assertEqual(rec.button, 'ACT')
        self.assertIsNone(rec.narrative)
        self.assertEqual({'type': 'task'}, rec.command)
        self.assertEqual(rec.context['foo'], 'bar')


class HyperlinkRecommendationTest(SDKBaseTest):
    def test___init__(self):
        rec = HyperlinkRecommendation(
            key='KEY!', rank=4, button='Try this', href='https://www.google.com/search?q=broccoli',
            title='Something needs to be done')
        self.assertIsInstance(rec, Recommendation)
        self.assertIsInstance(rec, Intervention)
        self.assertEqual(rec.key, 'KEY!')
        self.assertEqual(rec.title, 'Something needs to be done')
        self.assertEqual(rec.rank, 4)
        self.assertEqual(rec.button, 'Try this')
        self.assertEqual(rec.href, 'https://www.google.com/search?q=broccoli')


# --- helpers ---
class HelperCommand(SDKBaseTest):

    def equal_commands(self, expected: dict, result: dict):
        self.assertTrue(('type' in result) and (result['type'] == expected['type']))
        self.assertTrue(('filter' in result) and ('coding' in result['filter']))
        self.assertEqual(len(expected['filter']['coding']), len(result['filter']['coding']))

        for l_coding in expected['filter']['coding']:
            tmp = False
            for r_coding in result['filter']['coding']:
                if l_coding['system'] == r_coding['system']:
                    tmp = self.are_dicts_same(l_coding, r_coding)
                    break
            if not tmp:
                self.assertTrue(False, 'filter.coding with system: %s' % l_coding['system'])

    def are_dicts_same(self, left: dict, right: dict) -> bool:
        for key, val in left.items():
            result = False
            if key in right and isinstance(right[key], type(val)):
                if isinstance(val, dict):
                    result = self.are_dicts_same(val, right[key])
                elif isinstance(val, list):
                    result = True if sorted(val) == sorted(right[key]) else False
                else:
                    result = True if val == right[key] else False
            if not result:
                return False
        return True
