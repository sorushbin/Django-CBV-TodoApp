from rest_framework.routers import DefaultRouter
from . import views

app_name = "api-v1"

router = DefaultRouter()
router.register("task", views.TaskModelViewSet, basename="task")
urlpatterns = router.urls

# urlpatterns = [
#
#     path('task/', views.TaskModelViewSet.as_view({'get':'list', 'post':'create'}), name='task-list'),
#     path('task/<int:pk>/', views.TaskModelViewSet.as_view({'get':'retrieve', 'put':'update', 'patch':'partial_update', 'delete':'destroy'}), name='task-detail')

# ]
