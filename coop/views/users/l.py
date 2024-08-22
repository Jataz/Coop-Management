def registration_payment(request):
    user_data = request.session.get('user_data')
    beneficiary_data = request.session.get('beneficiary_data')

    if not user_data or not beneficiary_data:
        return redirect('signup')

    if request.method == 'POST':
        # Integrate payment gateway here
        payment_successful = True  # Replace with actual payment processing logic

        if payment_successful:
            # Create the user and beneficiary only after payment is successful
            user = CustomUser.objects.create(
                username=user_data['username'],
                email=user_data['email'],
                full_name=user_data['full_name'],
                phone_number=user_data['phone_number'],
                sex=user_data['sex'],
                id_number=user_data['id_number'],
                physical_address=user_data['physical_address'],
                date_of_birth=user_data['date_of_birth'],
                registration_fee_paid=True,
                is_member=True,
                password=make_password(user_data['password'])  # Hash the password before saving
            )

            Beneficiary.objects.create(
                user=user,
                **beneficiary_data
            )

            # Clear session data after successful payment
            request.session.pop('user_data', None)
            request.session.pop('beneficiary_data', None)
            messages.success(request, "Payment successful and details saved! You can now log in.")
            return redirect('/login')
        else:
            messages.error(request, "Payment failed. Please try again.")
            return redirect('registration-payment')

    return render(request, "accounts/payment.html")
