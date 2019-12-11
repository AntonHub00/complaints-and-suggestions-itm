from api.models import (
    ComplaintState,
    StrategicProcess,
    SubdivisionReponsible,
    Complaint,
    StudentComplaint,
    StaffComplaint,
    ExternalRelatedComplaint
)
from api.serializers import (
    ComplaintStateSerializer,
    StrategicProcessSerializer,
    SubdivisionReponsibleSerializer,
    ComplaintSerializer,
    StudentComplaintSerializer,
    StaffComplaintSerializer,
    ExternalRelatedComplaintSerializer
)

from datetime import datetime, timedelta

from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.response import Response


def calculate_tlp_date(given_date_string):
    days_to_add = 7
    given_date = datetime.strptime(given_date_string, '%Y-%m-%d').date()

    while days_to_add > 0:
        given_date += timedelta(days=1)
        if given_date.weekday() >= 5: # saturday = 5 and sunday = 6
            continue
        days_to_add -= 1
    return given_date.strftime('%Y-%m-%d')


def complaint_type_is_valid(complaint_type):
    return complaint_type in ['student', 'staff', 'external-related']


def get_object(complaint_type, pk=None):
    if pk is not None:
        if complaint_type == 'student':
            return get_object_or_404(StudentComplaint, complaint=pk)
        elif complaint_type == 'staff':
            return get_object_or_404(StaffComplaint, complaint=pk)
        else:
            return get_object_or_404(ExternalRelatedComplaint, complaint=pk)
    else:
        if complaint_type == 'student':
            return StudentComplaint.objects.all()
        elif complaint_type == 'staff':
            return StaffComplaint.objects.all()
        else:
            return ExternalRelatedComplaint.objects.all()


class ComplaintGetAllOfAllTypes(APIView):
    def get(self, request):
        payload = {}

        student_complaints = get_object('student')
        staff_complaints = get_object('staff')
        external_related_complaints = get_object('external-related')

        payload['students'] = StudentComplaintSerializer(student_complaints,
                                                         many=True).data
        payload['staff'] = StaffComplaintSerializer(staff_complaints,
                                                    many=True).data
        payload['extenal_related'] = ExternalRelatedComplaintSerializer(
            external_related_complaints,
            many=True).data

        return Response({'complaints' : payload})


class ComplaintGetAllOrCreateOfOneType(APIView):
    def get(self, request, complaint_type):
        payload = {}

        if not complaint_type_is_valid(complaint_type):
            return Response({'error': "only 'student', 'staff' and 'external-related'"
                             ' are available in the url'},
                            status=status.HTTP_404_NOT_FOUND)

        if complaint_type == 'student':
            student_complaints = get_object('student')
            payload = StudentComplaintSerializer(student_complaints,
                                                 many=True).data
        elif complaint_type == 'staff':
            staff_complaints = get_object('staff')
            payload = StaffComplaintSerializer(staff_complaints,many=True).data
        else:
            external_related_complaints = get_object('external-related')
            payload = ExternalRelatedComplaintSerializer(external_related_complaints,
                                                         many=True).data

        return Response({'complaints' : payload})


    def post(self, request, complaint_type):
        if not complaint_type_is_valid(complaint_type):
            return Response({'error': "only 'student', 'staff' and 'external-related'"
                             ' are available in the url'},
                            status=status.HTTP_404_NOT_FOUND)


        default_complaint_state = ComplaintState.objects.all().first()

        general_complaint = Complaint.objects.create(
            title=request.data['title'],
            complaint_state=default_complaint_state,
            name=request.data['name'],
            email=request.data['email'],
            phone=request.data['phone'],
            complaint_content=request.data['complaint_content']
        )

        if complaint_type == 'student':
            try:
                student_complaint = StudentComplaint.objects.create(
                    complaint=general_complaint,
                    control_number=request.data['control_number'],
                    career=request.data['career'],
                    semester=request.data['semester'],
                    group=request.data['group'],
                    turn=request.data['turn'],
                    classroom=request.data['classroom']
                )
            except Exception as e:
                print(e)
                general_complaint.delete()
                return Response({'error' : 'Student complaint could not be'
                                 ' created'}, status=status.HTTP_400_BAD_REQUEST)

            return Response({'succes' : 'Student complaint created succesfully'})
        elif complaint_type == 'staff':
            try:
                staff_complaint = StaffComplaint.objects.create(
                    complaint=general_complaint,
                    rfc=request.data['rfc'],
                    department=request.data['department']
                )
            except Exception as e:
                print(e)
                general_complaint.delete()
                return Response({'error' : 'Staff complaint could not be'
                                 ' created'}, status=status.HTTP_400_BAD_REQUEST)

            return Response({'succes' : 'Staff complaint created succesfully'})
        else:
            try:
                external_related_complaint = ExternalRelatedComplaint.objects.create(
                    complaint=general_complaint,
                    relation=request.data['relation']
                )
            except Exception as e:
                print(e)
                general_complaint.delete()
                return Response({'error' : 'External related complaint could'
                                 ' not be created'}, status=status.HTTP_400_BAD_REQUEST)

            return Response({'succes' : 'External related complaint created'
                             ' succesfully'})


class ComplaintGetAllOfOneType(APIView):
    def get(self, request, complaint_type, pk):
        payload = {}

        if not complaint_type_is_valid(complaint_type):
            return Response({'error': "only 'student', 'staff' and 'external-related'"
                             ' are available in the url'},
                            status=status.HTTP_404_NOT_FOUND)

        if complaint_type == 'student':
            payload = StudentComplaintSerializer(get_object(complaint_type,
                                                            pk)).data
        elif complaint_type == 'staff':
            payload = StaffComplaintSerializer(get_object(complaint_type,
                                                          pk)).data
        else:
            payload = ExternalRelatedComplaintSerializer(get_object(complaint_type,
                                                                    pk)).data

        return Response({'complaints' : payload})


class ComplaintGetAllRaw(APIView):
    def get(self, request):
        general_complaints = Complaint.objects.all()
        payload = ComplaintSerializer(general_complaints, many=True).data
        return Response({'complaints' : payload})


class ComplaintRaw(APIView):
    def get(self, request, pk):
        general_complaint = get_object_or_404(Complaint, pk=pk)
        payload = ComplaintSerializer(general_complaint).data
        return Response({'complaints' : payload})

    def patch(self, request, pk):
        general_complaint = get_object_or_404(Complaint, pk=pk)

        updatable_fields = {'complaint_state', 'opening_date',
                            'strategic_process', 'subdivision_responsible',
                            'responsible_delivery_date', 'tr_response_date',
                            'complainer_response_date'}

        # Checks if the given key is valid
        if not (set(request.data) <= updatable_fields):
            return Response({'error' : 'Only the following fields are available'
                             ' to be updated: complaint_state, opening_date,'
                             ' strategic_process, subdivision_responsible,'
                             ' responsible_delivery_date, responsible_response_date'
                             ' and complainer_response_date'},
                            status=status.HTTP_400_BAD_REQUEST)

        if 'complaint_state' in request.data:
            object = get_object_or_404(ComplaintState,
                                             pk=request.data['complaint_state'])
            general_complaint.complaint_state = object
        if 'opening_date' in request.data:
            general_complaint.opening_date = request.data['opening_date']
        if 'strategic_process' in request.data:
            object = get_object_or_404(StrategicProcess,
                                             pk=request.data['strategic_process'])
            general_complaint.strategic_process = object
        if 'subdivision_responsible' in request.data:
            object = get_object_or_404(SubdivisionReponsible,
                                             pk=request.data['subdivision_responsible'])
            general_complaint.subdivision_responsible = object
        if 'responsible_delivery_date' in request.data:
            general_complaint.responsible_delivery_date = request.data['responsible_delivery_date']
            general_complaint.tlp_response_date = calculate_tlp_date(request.data['responsible_delivery_date'])
        if 'tr_response_date' in request.data:
            general_complaint.tr_response_date = request.data['tr_response_date']
        if 'complainer_response_date' in request.data:
            general_complaint.complainer_response_date = request.data['complainer_response_date']

        general_complaint.save()

        return Response({'success' : 'Complaint updated succesfully'})


class StateGetAll(APIView):
    def get(self, request):
        complaint_states = ComplaintState.objects.all()
        payload = ComplaintStateSerializer(complaint_states, many=True).data
        return Response({'states' : payload})


class StrategicProcessGetAll(APIView):
    def get(self, request):
        strategic_processes = StrategicProcess.objects.all()
        payload = StrategicProcessSerializer(strategic_processes, many=True).data
        return Response({'strategic_processes' : payload})


class SubdivisionReponsibleGetAll(APIView):
    def get(self, request):
        subdivision_responsibles = SubdivisionReponsible.objects.all()
        payload = SubdivisionReponsibleSerializer(subdivision_responsibles, many=True).data
        return Response({'subdivision_responsibles' : payload})
