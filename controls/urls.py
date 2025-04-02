from django.urls import path
from controls.views import (
    signin,
    signup,
    signout,
)

urlpatterns = [
    path(route='signin/', view=signin, name='signin'),
    path(route='signup/', view=signup, name='signup'),
    path(route='signout/', view=signout, name='signout'),
]