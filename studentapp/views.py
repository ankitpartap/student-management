from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from .forms import CourseForm, EnrollmentForm, LoginForm, StudentForm
from .models import Course, Enrollment, Student


def home(request):
    return render(request, 'studentapp/home.html')


def custom_login(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            messages.success(request, 'Welcome back!')
            return redirect('dashboard')
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form})


@login_required(login_url='login')
def dashboard(request):
    total_students = Student.objects.count()
    total_courses = Course.objects.count()
    total_enrollments = Enrollment.objects.count()
    recent_enrollments = Enrollment.objects.select_related('student', 'course').order_by('-created_at')[:5]
    return render(request, 'studentapp/dashboard.html', {
        'total_students': total_students,
        'total_courses': total_courses,
        'total_enrollments': total_enrollments,
        'recent_enrollments': recent_enrollments,
    })


@login_required(login_url='login')
def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('home')


class StudentListView(LoginRequiredMixin, ListView):
    model = Student
    template_name = 'studentapp/student_list.html'
    context_object_name = 'students'
    paginate_by = 8

    def get_queryset(self):
        queryset = super().get_queryset().order_by('-created_at')
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(first_name__icontains=query) |
                Q(last_name__icontains=query) |
                Q(email__icontains=query) |
                Q(phone__icontains=query)
            )
        return queryset


class StudentCreateView(LoginRequiredMixin, CreateView):
    model = Student
    form_class = StudentForm
    template_name = 'studentapp/student_form.html'
    success_url = reverse_lazy('student-list')

    def form_valid(self, form):
        messages.success(self.request, 'Student added successfully.')
        return super().form_valid(form)


class StudentUpdateView(LoginRequiredMixin, UpdateView):
    model = Student
    form_class = StudentForm
    template_name = 'studentapp/student_form.html'
    success_url = reverse_lazy('student-list')

    def form_valid(self, form):
        messages.success(self.request, 'Student updated successfully.')
        return super().form_valid(form)


class StudentDeleteView(LoginRequiredMixin, DeleteView):
    model = Student
    template_name = 'studentapp/student_confirm_delete.html'
    success_url = reverse_lazy('student-list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Student deleted successfully.')
        return super().delete(request, *args, **kwargs)


class CourseListView(LoginRequiredMixin, ListView):
    model = Course
    template_name = 'studentapp/course_list.html'
    context_object_name = 'courses'
    paginate_by = 8

    def get_queryset(self):
        queryset = super().get_queryset().order_by('-created_at')
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(course_name__icontains=query) | Q(course_code__icontains=query)
            )
        return queryset


class CourseCreateView(LoginRequiredMixin, CreateView):
    model = Course
    form_class = CourseForm
    template_name = 'studentapp/course_form.html'
    success_url = reverse_lazy('course-list')

    def form_valid(self, form):
        messages.success(self.request, 'Course added successfully.')
        return super().form_valid(form)


class CourseUpdateView(LoginRequiredMixin, UpdateView):
    model = Course
    form_class = CourseForm
    template_name = 'studentapp/course_form.html'
    success_url = reverse_lazy('course-list')

    def form_valid(self, form):
        messages.success(self.request, 'Course updated successfully.')
        return super().form_valid(form)


class CourseDeleteView(LoginRequiredMixin, DeleteView):
    model = Course
    template_name = 'studentapp/course_confirm_delete.html'
    success_url = reverse_lazy('course-list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Course deleted successfully.')
        return super().delete(request, *args, **kwargs)


class EnrollmentListView(LoginRequiredMixin, ListView):
    model = Enrollment
    template_name = 'studentapp/enrollment_list.html'
    context_object_name = 'enrollments'
    paginate_by = 8

    def get_queryset(self):
        queryset = super().get_queryset().select_related('student', 'course').order_by('-created_at')
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(student__first_name__icontains=query) |
                Q(student__last_name__icontains=query) |
                Q(course__course_name__icontains=query)
            )
        return queryset


class EnrollmentCreateView(LoginRequiredMixin, CreateView):
    model = Enrollment
    form_class = EnrollmentForm
    template_name = 'studentapp/enrollment_form.html'
    success_url = reverse_lazy('enrollment-list')

    def form_valid(self, form):
        messages.success(self.request, 'Enrollment created successfully.')
        return super().form_valid(form)


class EnrollmentUpdateView(LoginRequiredMixin, UpdateView):
    model = Enrollment
    form_class = EnrollmentForm
    template_name = 'studentapp/enrollment_form.html'
    success_url = reverse_lazy('enrollment-list')

    def form_valid(self, form):
        messages.success(self.request, 'Enrollment updated successfully.')
        return super().form_valid(form)


class EnrollmentDeleteView(LoginRequiredMixin, DeleteView):
    model = Enrollment
    template_name = 'studentapp/enrollment_confirm_delete.html'
    success_url = reverse_lazy('enrollment-list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Enrollment deleted successfully.')
        return super().delete(request, *args, **kwargs)
