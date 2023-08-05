import json
import jwt
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token
from django.shortcuts import render
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .utils import get_tokens_for_user, decode
from .serializers import RegistrationSerializer, PasswordChangeSerializer
from .models import *
from .serializers import *
from rest_framework.response import Response

from .models import *
from .serializers import *
import datetime

SECRET = "my-secret"

# Create your views here.


def toJSON(thing):
    return json.dumps(thing, default=lambda o: o.__dict__, sort_keys=True, indent=4)


@api_view(["GET", "POST"])
def admin_list(req):
    if req.method == "GET":
        admin = Admin.objects.all()
        ser = AdminS(admin, many=True)

        return Response(ser.data)

    elif req.method == "POST":
        ser = AdminS(data=req.data)

        if ser.is_valid():
            ser.save()
        else:
            return Response("bad req")

        return Response(ser.data)


@api_view(["GET", "POST"])
def payment_list(req):
    if req.method == "GET":
        pay = Payment.objects.all()
        ser = PaymentS(pay, many=True)

        return Response(ser.data)

    elif req.method == "POST":
        ser = PaymentS2(data=req.data)

        if ser.is_valid():
            ser.save()
        else:
            return Response(
                {"message": "some thing went wrong"}, status=status.HTTP_400_BAD_REQUEST
            )

        return Response(ser.data)


@api_view(["PUT", "GET", "DELETE"])
def payment_one(req, id):
    found = Payment.objects.get(id=id)
    if req.method == "GET":
        ser = PaymentS(found)
        return Response(ser.data, status=status.HTTP_200_OK)

    if req.method == "PUT":
        ser = PaymentS(instance=found, data=req.data)

        if ser.is_valid():
            ser.save()
            return Response({"status": "your change ok"}, status=status.HTTP_200_OK)
        else:
            return Response(
                {"message": "some thins went wrong"}, status=status.HTTP_400_BAD_REQUEST
            )

    if req.method == "DELETE":
        found.delete()
        return Response(
            {"message": "pay data was successfuly deleted"},
            status=status.HTTP_202_ACCEPTED,
        )


@api_view(["GET", "POST"])
def teacher_list(req):
    if req.method == "GET":
        teacher = Teacher.objects.all()
        ser = TeacherS(teacher, many=True)

        return Response(ser.data)

    elif req.method == "POST":
        ser = TeacherS(data=req.data)

        if ser.is_valid():
            ser.save()
        else:
            return Response("bad req")

        return Response(ser.data)


@api_view(["GET"])
def week_list(req):
    if req.method == "GET":
        days = WeekDays.objects.all()
        ser = WeekDaysS(days, many=True)

        return Response(ser.data, status=status.HTTP_200_OK)


@api_view(["GET", "POST"])
def student_list(req):
    if req.method == "GET":
        students = Student.objects.all()
        ser = StudentS(students, many=True)

        return Response(ser.data)

    elif req.method == "POST":
        ser = StudentS(data=req.data)

        if ser.is_valid():
            ser.save()
        else:
            return Response(
                {"message": "Bad request"}, status=status.HTTP_400_BAD_REQUEST
            )

        return Response(ser.data)


@api_view(["GET", "POST"])
def technology_list(req):
    if req.method == "GET":
        technologies = Technology.objects.all()
        ser = TechnologyS(technologies, many=True)
        return Response(ser.data)

    elif req.method == "POST":
        ser = TechnologyS(data=req.data)
        if ser.is_valid():
            ser.save()
        else:
            return Response("bad req")
        return Response(ser.data)


@api_view(["GET", "POST"])
def davomat_list(req):
    if req.method == "GET":
        davomatlar = Davomat.objects.all()

        ser = DavomatS(davomatlar, many=True)
        return Response(ser.data)

    elif req.method == "POST":
        ser = DavomatS(data=req.data)

        if ser.is_valid():
            ser.save()
        else:
            return Response({"message": "bad req"}, status=status.HTTP_400_BAD_REQUEST)

        return Response(ser.data)


@api_view(["GET", "POST"])
def profession_list(req):
    if req.method == "GET":
        professions = Profession.objects.all()

        ser = ProfessionS(professions, many=True)

        return Response(ser.data)

    elif req.method == "POST":
        ser = ProfessionS(data=req.data)
        if ser.is_valid():
            ser.save()
        else:
            return Response("bad req")

        return Response(ser.data)


@api_view(["GET", "POST"])
def groups_list(req):
    if req.method == "GET":
        groups = Groups.objects.all()
        ser = GroupsS(groups, many=True)
        return Response(ser.data)

    if req.method == "POST":
        ser = GroupsS2(data=req.data)
        if ser.is_valid():
            ser.save()
        else:
            return Response(
                {"message": "some things went wrong"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(ser.data, status=status.HTTP_200_OK)


@api_view(["GET", "POST"])
def direcktor_list(req):
    if req.method == "GET":
        direcktrs = Director.objects.all()
        ser = DireactorS(direcktrs, many=True)
        return Response(ser.data)

    elif req.method == "POST":
        ser = DireactorS(data=req.data)
        if ser.is_valid():
            ser.save()
        else:
            return Response("bad request")

        return Response(ser.data)


@api_view(["GET", "PUT", "DELETE"])
def direcktor_detail(req, id):
    try:
        direktor = Director.objects.get(id=id)
    except:
        return Response("item doesn't exist")

    if req.method == "GET":
        ser = DireactorS(direktor)
        return Response(ser.data)

    elif req.method == "PUT":
        ser = DireactorS(instance=direktor, data=req.data)
        if ser.is_valid():
            ser.save()
        else:
            return Response("bad request")
        return Response(ser.data)

    elif req.method == "DELETE":
        direktor.delete()
        return Response("item has deleted")


@api_view(["GET", "PUT", "DELETE"])
def davomat_detail(req, id):
    try:
        davomat = Davomat.objects.get(id=id)
    except:
        return Response({"message": "item doesn't exist"}, status=status.HTTP_400_BAD_REQUEST)

    if req.method == "GET":
        ser = DavomatS(davomat)

        return Response(ser.data)
    elif req.method == "PUT":
        ser = DavomatS(instance=davomat, data=req.data)
        if ser.is_valid():
            ser.save()
        else:
            return Response({"message": "bad"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(ser.data)

    elif req.method == "DELETE":
        davomat.delete()

        return Response("item has deleted")


@api_view(["GET", "PUT", "DELETE"])
def student_detail(req, id):
    try:
        student = Student.objects.get(id=id)
    except:
        return Response("item doesn't exist")
    if req.method == "GET":
        ser = StudentS(student)
        return Response(ser.data)
    elif req.method == "PUT":
        ser = StudentS(instance=student, data=req.data)
        if ser.is_valid():
            ser.save()
        return Response(ser.data)
    elif req.method == "DELETE":
        student.delete()
        return Response("item has deleted")


@api_view(["GET", "PUT", "DELETE"])
def technology_detail(req, id):
    try:
        technology = Technology.objects.get(id=id)
    except:
        return Response("item doesn't exist")

    if req.method == "GET":
        ser = TechnologyS(technology)
        return Response(ser.data)

    if req.method == "PUT":
        ser = TechnologyS(instance=technology, data=req.data)

        if ser.is_valid():
            ser.save()
        else:
            return Response("bad req")

        return Response(ser.data)

    if req.method == "DELETE":
        technology.delete()
        return Response("item has deleted")


@api_view(["GET", "PUT", "DELETE"])
def profession_detail(req, id):
    try:
        profession = Profession.objects.get(id=id)
    except:
        return Response("item doesn't exist")

    if req.method == "GET":
        ser = ProfessionS(profession)
        return Response(ser.data)

    elif req.method == "PUT":
        ser = ProfessionS(instance=profession, data=req.data)
        if ser.is_valid():
            ser.save()
        else:
            return Response("bad req")

        return Response(ser.data)

    elif req.method == "DELETE":
        profession.delete()
        return Response("item has deleted")


@api_view(["GET", "PUT", "DElETE"])
def groups_detail(req, id):
    try:
        group = Groups.objects.get(id=id)
    except:
        return Response("item doesn't exist")

    if req.method == "GET":
        ser = GroupsS(group)

        return Response(ser.data)

    elif req.method == "PUT":
        ser = GroupsS2(instance=group, data=req.data)

        if ser.is_valid():
            ser.save()
        else:
            return Response(
                {"message": "what is shit"}, status=status.HTTP_400_BAD_REQUEST
            )

        return Response(ser.data)

    elif req.method == "DELETE":
        group.delete()
        return Response({"message": "item has deleted"}, status=status.HTTP_202_ACCEPTED)


@api_view(["GET", "PUT", "DELETE"])
def teacher_detail(req, id):
    try:
        teacher = Teacher.objects.get(id=id)
    except:
        return Response("item doesn't exist")
    if req.method == "GET":
        ser = TeacherS(teacher)
        return Response(ser.data)
    elif req.method == "PUT":
        ser = TeacherS(instance=teacher, data=req.data)
        if ser.is_valid():
            ser.save()
        return Response(ser.data)
    elif req.method == "DELETE":
        teacher.delete()
        return Response("item has deleted")


@api_view(["GET", "PUT", "DELETE"])
def admin_detail(req, id):
    if req.data["role"] == "DR" or req.data["role"] == "DIRECTOR":
        try:
            admin = Admin.objects.get(id=id)
        except:
            return Response("item doesn't exist")
        if req.method == "GET":
            ser = AdminS(admin)
            return Response(ser.data)
        elif req.method == "PUT":
            ser = AdminS(instance=admin, data=req.data)
            if ser.is_valid():
                ser.save()
            return Response(ser.data)
        elif req.method == "DELETE":
            admin.delete()
            return Response("item has deleted")


class RegistrationView(APIView):
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        print(RegistrationSerializer.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(request.data)
        username = serializer.data.get("username")
        password = serializer.data.get("password")
        role = serializer.data.get("role")
        if role == "DR" or role == "DIRECTOR":
            try:
                director = Director.objects.get(username=username)
                ser = DireactorS(director)
                token = get_tokens_for_user(
                    {"username": director.username, "role": role}
                )

                if director.password != password:
                    return Response(
                        {"message": "Parol xato terilgan"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                return Response({"token": token, "user": ser.data, "role": role})
            except:
                return Response(
                    {"message": "Director topilmadi"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        if role == "AD" or role == "ADMINISTRATOR":
            try:
                adminstator = Admin.objects.get(username=username)
                token = get_tokens_for_user(
                    {"username": adminstator.username, "role": role}
                )
                ser = AdminS(adminstator)

                if adminstator.password != password:
                    return Response(
                        {"message": "Parol xato terilgan"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                return Response({"token": token, "user": ser.data, "role": role})
            except:
                return Response(
                    {"message": "Adminstator topilmadi"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        if role == "TR" or role == "TEACHER":
            try:
                teacher = Teacher.objects.get(username=username)
                tokenS = get_tokens_for_user(
                    {"username": teacher.username, "role": role}
                )
                ser = TeacherS(teacher)

                if teacher.password != password:
                    return Response(
                        {"message": "Parol xato terilgan"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                return Response({"token": tokenS, "user": ser.data, "role": role})
            except teacher.DoesNotExist:
                return Response({"message": "O'qituvchi topilmadi"})
        if role == "ST" or role == "STUDENT":
            try:
                student = Student.objects.get(username=username)
                tokenS = get_tokens_for_user(
                    {"username": student.username, "role": role}
                )
                ser = StudentS(instance=student)
                if student.password != password:
                    return Response(
                        {"message": "Parol xato terilgan"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                return Response({"token": tokenS, "user": ser.data, "role": role})
            except:
                return Response(
                    {"message": "O'quvchi topilmadi"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        return Response(
            {"msg": "Invalid Credentials"}, status=status.HTTP_401_UNAUTHORIZED
        )


class LogoutView(APIView):
    def post(self, request):
        logout(request)
        return Response({"msg": "Successfully Logged out"}, status=status.HTTP_200_OK)


class ChangePasswordView(APIView):
    permission_classes = [
        IsAuthenticated,
    ]

    def post(self, request):
        serializer = PasswordChangeSerializer(
            context={"request": request}, data=request.data
        )
        serializer.is_valid(
            raise_exception=True
        )  # Another way to write is as in Line 17
        request.user.set_password(serializer.validated_data["new_password"])
        request.user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["GET"])
def get_user(req, token):
    result = decode(token=token)
    username = result["payload"]["username"]
    role = result["payload"]["role"]
    if role == "DR" or role == "DIRECTOR":
        director = Director.objects.get(username=username)
        ser = DireactorS(director)
        token = get_tokens_for_user({"username": director.username, "role": role})
        return Response({"token": token, "user": ser.data, "role": role})
    if role == "AD" or role == "ADMINISTRATOR":
        adminstator = Admin.objects.get(username=username)
        token = get_tokens_for_user(adminstator.username)
        ser = AdminS(adminstator)
        return Response({"token": token, "user": ser.data, "role": role})
    if role == "TR" or role == "TEACHER":
        teacher = Teacher.objects.get(username=username)
        tokenS = get_tokens_for_user(teacher.username)
        ser = TeacherS(teacher)
        return Response({"token": tokenS, "user": ser.data, "role": role})
    if role == "ST" or role == "STUDENT":
        student = Student.objects.get(username=username)
        tokenS = get_tokens_for_user({"username": student.username, "role": role})
        ser = StudentS(instance=student)
        return Response({"token": tokenS, "user": ser.data, "role": role})
    return Response(
        {"message": "something went to wrong"},
        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )


@api_view(["GET"])
def getUser(req, id, role):
    if role == "ST" or role == "STUDENT":
        student = Student.objects.get(id=id)
        serailizer = StudentS(instance=student)
        return Response(serailizer.data, status=status.HTTP_200_OK)
    if role == "TR" or role == "TEACHER":
        teacher = Teacher.objects.get(id=id)
        serailizer = TeacherS(instance=teacher)
        return Response(serailizer.data, status=status.HTTP_200_OK)
    if role == "AD" or role == "ADMINISTRATOR":
        adminstator = Admin.objects.get(id=id)
        serializer = AdminS(instance=adminstator)
        return Response(serailizer.data, status=status.HTTP_200_OK)
    if role == "DR" or role == "DIRECTOR":
        director = Director.objects.get(id=id)
        serailizer = DireactorS(instance=director)
        return Response(serializer.data, status=status.HTTP_200_OK)
