from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('grappelli/', include('grappelli.urls')),  # Grappelli admin URLs
    path('admin/', admin.site.urls),
    path('api/order/', include("order.urls")),
    path('api/accounts/', include("accounts.urls")),
    path('api/blog/', include("blog.urls")),
    path('api/payment/', include("payment.urls")),
]
