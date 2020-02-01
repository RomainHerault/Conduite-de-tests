from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout

# Create your views here.
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test

from StoreManager.models import Product, Department, User
from StoreManager.models import Employee
from . import forms


def index(request):
    return HttpResponse("Coucou Djangooooooooooooooooo !")


@login_required
def rayon(request):
    error = False
    error_message = ""
    superuser = request.user.is_superuser
    if request.method == 'POST' and request.POST.get('add'):  # check if post request comes from correct button
        if not Product.objects.filter(name="").exists():
            if superuser:
                try:
                    default_dep = Department.objects.get(name="")
                except:
                    default_dep = Department(name="", store_id="1")
                    default_dep.save()
                new_product = Product(name="", quantity=0, ref="", price=0.0,
                                      department_id=default_dep.id)
            else:
                new_product = Product(name="", quantity=0, ref="", price=0.0,
                                      department_id=request.user.employee.department.id)
            if not error:
                new_product.save()
        else :
            error = True,
            error_message = "un employé par défaut existe déjà"

    elif request.method == 'POST' and request.POST.get(
            'modify'):  # check if post request comes from correct button

        selected_products_id = request.POST.getlist('action_product')

        id_products = list(Product.objects.values_list('id', flat=True))
        id_products.sort()

        name_products = request.POST.getlist('name_product')
        price_products = request.POST.getlist('price_product')
        quantity_products = request.POST.getlist('quantity_product')
        ref_products = request.POST.getlist('ref_product')

        if superuser:
            departments = request.POST.getlist('department')

        for product_id in selected_products_id:

            product = Product.objects.get(pk=product_id)
            if not superuser and product.department.id is not request.user.employee.department.id:
                error = True,
                error_message = "Vous ne pouvez pas modifier tous les produits séléctionnés (mauvais département)"
            else:
                product.name = name_products[id_products.index(int(product_id))]
                product.price = price_products[id_products.index(int(product_id))]
                product.quantity = quantity_products[id_products.index(int(product_id))]
                product.ref = ref_products[id_products.index(int(product_id))]
                if superuser:
                    department_name = departments[id_products.index(int(product_id))]
                    try:
                        dep = Department.objects.get(name=department_name)
                        product.department = dep
                    except:
                        error, error_message = True, "le département n'existe pas"
                if not error:
                    error, error_message = product.doesRefExists()
                    if not error:
                        error, error_message = product.isNotValid()
                        if not error:
                            product.save()

    elif request.method == 'POST' and request.POST.get(
            'delete'):  # check if post request comes from correct button

        selected_products = request.POST.getlist('action_product')  # get id of selected products
        for product in Product.objects.filter(id__in=selected_products):
            if product.department.id is not request.user.employee.department.id and not superuser:
                error = True,
                error_message = "Vous ne pouvez pas supprimer tous les produits séléctionnés (mauvais département)"
            else:
                product.delete()

    header = ['Action', 'Nom', 'Prix', 'Quantité', 'Ref', 'Nom Rayon']
    query_results = Product.objects.all()  # TODO à modifier en fonction des droits du user
    return render(request, 'StoreManager/rayon.html',
                  {'username': request.user.username, 'header': header, 'data': query_results, 'error': error,
                   'error_message': error_message, 'superuser': superuser})


@login_required
def departement(request):
    error = False
    error_message = ""
    if request.user.is_superuser:
        if request.method == 'POST' and request.POST.get('add'):  # check if post request comes from correct button
            if not Department.objects.filter(name="").exists():
                new_dep = Department(name="", store_id=1)
                new_dep.save()
            else :
                error = True
                error_message = "un département par défaut existe déjà"
        elif request.method == 'POST' and request.POST.get(
                'modify'):  # check if post request comes from correct button

            selected_dep_id = request.POST.getlist('action_dep')

            id_deps = list(Department.objects.values_list('id', flat=True))
            id_deps.sort()

            print(id_deps)

            dep_name = request.POST.getlist('dep_name')

            username = request.POST.getlist('username')

            for dep_id in selected_dep_id:
                dep = Department.objects.get(pk=dep_id)
                dep.name = dep_name[id_deps.index(int(dep_id))]
                error, error_message = dep.doesNameExists()
                if not error:
                    dep.save()

                if username[id_deps.index(int(dep_id))]:
                    try:
                        user = User.objects.get(username=username[id_deps.index(int(dep_id))])
                        employee = Employee.objects.get(user=user)
                        employee.department = dep
                        employee.save()
                    except:
                        error = True
                        error_message = "l'employé n'existe pas"


        elif request.method == 'POST' and request.POST.get(
                'delete'):  # check if post request comes from correct button

            selected_dep = request.POST.getlist('action_dep')  # get id of selected products
            Department.objects.filter(id__in=selected_dep).delete()  # delete selected product

        header = ['Action', 'Departement', "Nom d'utilisateur"]
        query_employee_results = Employee.objects.all().select_related()
        query_dept = Department.objects.all()

        custom_data = []

        for dept in query_dept:
            for emp in query_employee_results:
                if dept.name == emp.department.name:
                    custom_data.append([dept, emp])
            if custom_data[-1][0].name != dept.name:
                custom_data.append([dept])
        return render(request, 'StoreManager/departement.html',
                      {'username': request.user.username, 'header': header, 'data': custom_data, 'error': error,
                       'error_message': error_message})
    else:
        return render(request, 'StoreManager/forbiddenAccess.html', locals())


@login_required
def employe(request):
    error = False
    error_message = ""

    if request.user.is_superuser:
        if request.method == 'POST' and request.POST.get('add'):  # check if post request comes from correct button
            if not User.objects.filter(username = "default_username").exists() :
                new_user = User.objects.create_user(username="default_username", password="password", email="")
                new_user.save()
                try:
                    default_dep = Department.objects.get(name="")
                except:
                    default_dep = Department(name="", store_id="1")
                    default_dep.save()
                new_emp = Employee(user=new_user, phonenumber="", department_id=default_dep.id)
                new_emp.save()
            else:
                error, error_message = True, "un employé par défaut existe déjà"
        elif request.method == 'POST' and request.POST.get(
                'modify'):  # check if post request comes from correct button

            selected_emp_id = request.POST.getlist('action_user')

            id_employees = list(Employee.objects.values_list('id', flat=True))
            id_employees.sort()

            username = request.POST.getlist('name_user')
            password = request.POST.getlist('password_user')
            phone = request.POST.getlist('phone_user')
            email = request.POST.getlist('email_user')
            dep = request.POST.getlist('dept_user')

            for emp_id in selected_emp_id:
                emp = Employee.objects.get(pk=emp_id)
                emp.user.username = username[id_employees.index(int(emp_id))]  # TODO check if username already exist
                error, error_message = emp.doesNameExists()

                emp.user.set_password(password[id_employees.index(int(emp_id))])
                emp.phonenumber = phone[id_employees.index(int(emp_id))]
                emp.user.email = email[id_employees.index(int(emp_id))]
                try :
                    emp.department = Department.objects.get(
                        name=dep[id_employees.index(int(emp_id))])
                except :
                    error, error_message = True, "département invalide"
                if not error :
                    emp.user.save()
                    emp.save()


        elif request.method == 'POST' and request.POST.get(
                'delete'):  # check if post request comes from correct button

            selected_emp = request.POST.getlist('action_user')
            employees_to_delete = Employee.objects.filter(id__in=selected_emp).select_related()

            for employee in employees_to_delete:
                employee.user.delete()
                employee.delete()

        header = ['Action', "Nom d'utilisateur", 'Mot de passe', 'Téléphone', 'Email', 'Departement',
                  'Date de création']
        query_employee_results = Employee.objects.all().select_related()

        return render(request, 'StoreManager/employee.html',
                      {'username': request.user.username, 'header': header, 'data': query_employee_results,'error': error,
                       'error_message': error_message})

    else:
        return render(request, 'StoreManager/forbiddenAccess.html', locals())


def connexion(request):
    error = False
    if request.method == "POST":
        form = forms.ConnexionForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(username=username, password=password)  # Nous vérifions si les données sont correctes
            if user:  # Si l'objet renvoyé n'est pas None
                login(request, user)  # nous connectons l'utilisateur
                if 'next' in request.GET:
                    next = request.GET['next']
                    if next is not None:
                        return redirect(next)
            else:  # sinon une erreur sera affichée
                error = True
    else:
        form = forms.ConnexionForm()

    return render(request, 'StoreManager/login.html', locals())


def deconnexion(request):
    logout(request)
    return redirect(reverse(connexion))
