from App.models.movie_user.customers import CustomerModel


def get_customer(custom_id):
    user = CustomerModel.query.get(custom_id)
    if user:
        return user
    elif CustomerModel.query.filter(CustomerModel.phone == custom_id).first():
        user = CustomerModel.query.filter(CustomerModel.phone == custom_id).first()
        return user
    elif CustomerModel.query.filter(CustomerModel.name == custom_id).first():
        user = CustomerModel.query.filter(CustomerModel.name == custom_id).first()

        return user
    else:
        return False