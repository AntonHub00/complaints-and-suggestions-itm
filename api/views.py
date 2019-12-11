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

from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.response import Response


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

        general_complaint = Complaint.objects.create(
            name=request.data['name'],
            email=request.data['email'],
            phone=request.data['phone'],
            complaint_content=request.data['complaint_content']
        )

        if complaint_type == 'student':
            student_complaint.create(
                complaint=general_complaint,
                control_number=request.data['control_number'],
                career=request.data['career'],
                semester=request.data['semester'],
                group=request.data['group'],
                turn=request.data['turn'],
                classroom=request.data['classroom']
            )

            return Response({'succes' : 'Student complaint created succesfully'})
        elif complaint_type == 'staff':
            staff_complaint = StaffComplaint.objects.create(
                complaint=general_complaint,
                rfc=request.data['rfc'],
                department=request.data['department']
            )

            return Response({'succes' : 'Staff complaint created succesfully'})
        else:
            external_related_complaint = ExternalRelatedComplaint.objects.create(
                complaint=general_complaint,
                relation=request.data['relation']
            )

            return Response({'succes' : 'Staff complaint created succesfully'})


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

        if 'complaint_state' in request.data:
            pass
        elif 'opening_date' in request.data:
            pass
        elif 'strategic_process' in request.data:
            pass
        elif 'subdivision_responsible' in request.data:
            pass
        elif 'responsible_delivery_date' in request.data:
            pass
        elif 'responsible_response_date' in request.data:
            pass
        elif 'complainer_response_date' in request.data:
            pass
        else:
            return Response({'error' : 'Only the following fields are available'
                             ' to be updated: complaint_state, opening_date,'
                             ' strategic_process, subdivision_responsible,'
                             ' responsible_delivery_date, responsible_response_date'
                             ' and complainer_response_date'},
                            status=status.HTTP_400_BAD_REQUEST)

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
