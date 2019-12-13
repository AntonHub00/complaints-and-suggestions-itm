from django.urls import path, include
from api.views import (
    ComplaintGetAllOfAllTypes,
    ComplaintGetAllOrCreateOfOneType,
    ComplaintGetAllOfOneType,
    ComplaintGetAllRaw,
    ComplaintRaw,
    StateGetAll,
    StrategicProcessGetAll,
    SubdivisionReponsibleGetAll,
    AuthenticateUser,
)

urlpatterns = [
    # Retrieves all the fields and instances of all types of complaints
    path('complaints/', ComplaintGetAllOfAllTypes.as_view(),
         name='api-complaint-get-all-of-all-types'),

    # Retrieves all the fields and instances of a specific type of complaint
    # or creates one with the complaint type given
    path('complaints/<complaint_type>/', ComplaintGetAllOrCreateOfOneType.as_view(),
         name='api-complaint-get-create-one-type'),

    # Retrieves all the fields of a specific complaint with the pk given (one instance)
    path('complaints/<complaint_type>/<int:pk>', ComplaintGetAllOfOneType.as_view(),
         name='api-complaint-get-all-of-one-type'),

    # Retrieves just the fields of all general complaints
    path('complaints-raw/', ComplaintGetAllRaw.as_view(),
         name='api-get-all-raw'),

    # Retrieves just the fields of a general complaint with the pk given (one instance)
    # or updates one with the complaint type given
    path('complaints-raw/<int:pk>', ComplaintRaw.as_view(),
         name='api-complaint-raw'),

    # Retrieves all the fields and instances of all complaint states
    path('states/', StateGetAll.as_view(),
         name='api-state-get-all'),

    # Retrieves all the fields and instances of all strategic processes
    path('strategic-processes/', StrategicProcessGetAll.as_view(),
         name='api-strategic-processes-get-all'),

    # Retrieves all the fields and instances of all subdivision responsibles
    path('subdivision-responsibles/', SubdivisionReponsibleGetAll.as_view(),
         name='api-subdivision-responsibles-get-all'),

    # Retrieves true if the username and password are correct, otherwise false
    path('authenticate-user/', AuthenticateUser.as_view(),
         name='api-authenticate-user'),
]
