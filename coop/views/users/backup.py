def signupp(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully! An OTP was sent to your Email")
            return redirect("verify-email", username=request.POST['username'])
    context = {"form": form}
    return render(request, "accounts/signup.html", context)

def registration_payment1(request):
    user_data = request.session.get('user_data')
    beneficiary_data_list = request.session.get('beneficiary_data')

    # Check that user and beneficiary data exist in session
    if not user_data or not beneficiary_data_list:
        return redirect('signup')

    if request.method == 'POST':
        # Integrate payment gateway here
        payment_successful = True  # Replace with actual payment processing logic

        if payment_successful:
            try:
                # Create the user after payment is confirmed
                user = CustomUser(
                    username=user_data['username'],
                    email=user_data['email'],
                    full_name=user_data['full_name'],
                    phone_number=user_data['phone_number'],
                    sex=user_data['sex'],
                    id_number=user_data['id_number'],
                    physical_address=user_data['physical_address'],
                    date_of_birth=user_data['date_of_birth'],
                    registration_fee_paid=True,
                    is_member=True
                )
                user.set_password(user_data['password'])  # Hash the password before saving
                user.save()

                # Create beneficiaries linked to this user
                for beneficiary_data in beneficiary_data_list:
                    Beneficiary.objects.create(
                        user=user,
                        **beneficiary_data
                    )

                # Clear session data after a successful transaction
                request.session.pop('user_data', None)
                request.session.pop('beneficiary_data', None)

                messages.success(request, "Payment successful and details saved! You can now log in.")
                return redirect('/login')

            except Exception as e:
                # Handle potential errors during user creation
                messages.error(request, f"An error occurred: {str(e)}")
                return redirect('registration-payment')

        else:
            messages.error(request, "Payment failed. Please try again.")
            return redirect('registration-payment')

    return render(request, "accounts/payment.html")