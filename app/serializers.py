from rest_framework import serializers
from .models import *


class TechnologyS(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Technology


class ProfessionS(serializers.ModelSerializer):
    technologies = TechnologyS(many=True, read_only=True)

    class Meta:
        fields = "__all__"
        model = Profession


class DavomatS(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Davomat


class AdminS(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Admin

    def create(self, validate_data):
        admin = Admin.objects.create(**validate_data)
        return admin

    def update(self, instance, validate_data):
        instance.name = validate_data.get("name", instance.name)
        instance.surname = validate_data.get("surname", instance.surname)
        instance.username = validate_data.get("username", instance.username)
        instance.password = validate_data.get("password", instance.password)
        instance.save()

        return instance


class TeacherS(serializers.ModelSerializer):
    profession = ProfessionS(many=True, read_only=True)
    profession_id = serializers.PrimaryKeyRelatedField(
        write_only=True, many=True, queryset=Profession.objects.all()
    )
    technologies_id = serializers.PrimaryKeyRelatedField(
        write_only=True, many=True, queryset=Technology.objects.all()
    )

    technologies = TechnologyS(many=True, read_only=True)

    class Meta:
        fields = "__all__"
        model = Teacher

    def create(self, validate_data):
        professions = validate_data.pop("profession_id")
        technologies = validate_data.pop("technologies_id")
        teacher = Teacher.objects.create(**validate_data)
        if professions:
            teacher.profession.set(professions)
        if technologies:
            teacher.technologies.set(technologies)
        return teacher

    def update(self, instance, validate_data):
        instance.name = validate_data.get("name", instance.name)
        instance.surname = validate_data.get("surname", instance.surname)
        instance.username = validate_data.get("username", instance.username)
        instance.salary = validate_data.get("salary", instance.salary)
        instance.save()

        professions = validate_data.pop("profession_id")
        technologies = validate_data.pop("technologies_id")
        if professions:
            instance.profession.set(professions)

        if technologies:
            instance.technologies.set(technologies)

        return instance


class StudentS(serializers.ModelSerializer):
    profession = ProfessionS(many=True, read_only=True)
    technologies = TechnologyS(many=True, read_only=True)
    teachers = TeacherS(many=True, read_only=True)
    davomat = DavomatS(many=True, read_only=True)
    profession_id = serializers.PrimaryKeyRelatedField(
        write_only=True, many=True, queryset=Profession.objects.all()
    )
    teachers_id = serializers.PrimaryKeyRelatedField(
        write_only=True, many=True, queryset=Teacher.objects.all()
    )

    class Meta:
        fields = "__all__"
        model = Student

    def create(self, validate_data):
        professions = validate_data.pop("profession_id")
        teachers = validate_data.pop("teachers_id")

        student = Student.objects.create(**validate_data)

        if professions:
            student.profession.set(professions)
        if teachers:
            student.teachers.set(teachers)
        return student

    def update(self, instance, validate_data):
        instance.name = validate_data.get("name", instance.name)
        instance.surname = validate_data.get("surname", instance.surname)
        instance.phone = validate_data.get("phone", instance.phone)
        instance.save()

        professions = validate_data.pop("profession_id")
        teachers = validate_data.pop("teachers_id")

        if professions:
            instance.profession.set(professions)
        if teachers:
            instance.teachers.set(teachers)
        return instance


class WeekDaysS(serializers.ModelSerializer):
    class Meta:
        model = WeekDays
        fields = "__all__"


class GroupsS2(serializers.ModelSerializer):
    week_days = WeekDaysS(many=True, read_only=True)
    technologies = TechnologyS(many=True, read_only=True)
    students = StudentS(many=True, read_only=True)
    week_days_id = serializers.PrimaryKeyRelatedField(
        write_only=True, many=True, queryset=WeekDays.objects.all()
    )
    technologies_id = serializers.PrimaryKeyRelatedField(
        write_only=True, many=True, queryset=Technology.objects.all()
    )
    students_id = serializers.PrimaryKeyRelatedField(
        write_only=True, many=True, queryset=Student.objects.all()
    )

    class Meta:
        model = Groups
        fields = "__all__"

    def create(self, validate_data):
        week_days = validate_data.pop("week_days_id")
        technologies = validate_data.pop("technologies_id")
        students2 = validate_data.pop("students_id")
        group = Groups.objects.create(**validate_data)
        group.save()
        if week_days:
            group.week_days.set(week_days)
        if technologies:
            group.technologies.set(technologies)
        if students2:
            group.students.set(students2)
        return group

    def update(self, instance, validate_data):
        week_days = validate_data.pop("week_days_id")
        technologies = validate_data.pop("technologies_id")
        students = validate_data.pop("students_id")

        instance.name = validate_data.get("name", instance.name)
        instance.price = validate_data.get("price", instance.price)
        instance.begin_date = validate_data.get("begin_date", instance.begin_date)
        instance.complete_date = validate_data.get(
            "complete_date", instance.complete_date
        )
        instance.when_start = validate_data.get("when_start", instance.when_start)
        instance.teacher = validate_data.get("teacher", instance.teacher)
        instance.save()

        if week_days:
            instance.week_days.set(week_days)
        if technologies:
            instance.technologies.set(technologies)
        if students:
            instance.students.set(students)

        return instance


class GroupsS(serializers.ModelSerializer):
    week_days = WeekDaysS(many=True, read_only=True)
    technologies = TechnologyS(many=True, read_only=True)
    students = StudentS(many=True, read_only=True)
    week_days_id = serializers.PrimaryKeyRelatedField(
        write_only=True, many=True, queryset=WeekDays.objects.all()
    )
    technologies_id = serializers.PrimaryKeyRelatedField(
        write_only=True, many=True, queryset=Technology.objects.all()
    )
    students_id = serializers.PrimaryKeyRelatedField(
        write_only=True, many=True, queryset=Student.objects.all()
    )
    teacher = TeacherS()

    class Meta:
        model = Groups
        fields = "__all__"

    def create(self, validate_data):
        week_days = validate_data.pop("week_days_id")
        technologies = validate_data.pop("technologies_id")
        students2 = validate_data.pop("students_id")
        group = Groups.objects.create(**validate_data)
        group.save()
        if week_days:
            group.week_days.set(week_days)
        if technologies:
            group.technologies.set(technologies)
        if students2:
            group.students.set(students2)
        return group

    def update(self, instance, validate_data):
        week_days = validate_data.pop("week_days_id")
        technologies = validate_data.pop("technologies_id")
        students = validate_data.pop("students_id")

        instance.name = validate_data.get("name", instance.name)
        instance.price = validate_data.get("price", instance.price)
        instance.period = validate_data.get("period", instance.period)
        instance.begin_date = validate_data.get("begin_date", instance.begin_date)
        instance.complete_date = validate_data.get(
            "complete_date", instance.complete_date
        )
        instance.teacher = validate_data.get("teacher", instance.teacher)
        instance.save()

        if week_days:
            instance.week_days.set(week_days)
        if technologies:
            instance.technologies.set(technologies)
        if students:
            instance.students.set(students)

        return instance


class DireactorS(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Director


class PaymentS(serializers.ModelSerializer):
    teacher = TeacherS()
    student = StudentS()
    group = GroupsS()
    administrator = AdminS()

    class Meta:
        fields = "__all__"
        model = Payment

    def create(self, validate_data):
        pay = Payment.objects.create(**validate_data)
        return pay


class PaymentS2(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Payment

    def create(self, validate_data):
        pay = Payment.objects.create(**validate_data)
        return pay


from rest_framework import serializers
from .models import MyUser


class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ["username", "password", "role"]


class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={"input_type": "password"}, write_only=True)

    class Meta:
        model = MyUser
        fields = ["email", "username", "password", "password2", "role"]
        extra_kwargs = {"password": {"write_only": True}}

    def save(self):
        user = MyUser(
            email=self.validated_data["email"],
            date_of_birth=self.validated_data["date_of_birth"],
        )
        password = self.validated_data["password"]
        password2 = self.validated_data["password2"]
        if password != password2:
            raise serializers.ValidationError({"password": "Passwords must match."})
        user.set_password(password)
        user.save()
        return user


class PasswordChangeSerializer(serializers.Serializer):
    current_password = serializers.CharField(
        style={"input_type": "password"}, required=True
    )
    new_password = serializers.CharField(
        style={"input_type": "password"}, required=True
    )

    def validate_current_password(self, value):
        if not self.context["request"].user.check_password(value):
            raise serializers.ValidationError({"current_password": "Does not match"})
        return value


# [
#     {
#         "name":"frontend",
#         "technologies":[
#             {}
#         ]
#     }
# ]
