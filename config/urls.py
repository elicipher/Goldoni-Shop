"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path , include
# from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
<<<<<<< HEAD
from drf_yasg.generators import OpenAPISchemaGenerator

class CustomOpenAPISchemaGenerator(OpenAPISchemaGenerator):
  def get_schema(self, request=None, public=False):
    """Generate a :class:`.Swagger` object with custom tags"""

    swagger = super().get_schema(request, public)
    swagger.tags = [
        {
            "name": "api",
            "description": "everything about your API"
        },
        {
            "name": "users",
            "description": "everything about your users"
        },
    ]

    return swagger
=======

>>>>>>> edb947b97584b34cbe74bc837c3a16415359efa5



schema_view = get_schema_view(
   openapi.Info(
<<<<<<< HEAD
      title="Goldoni API",
      default_version='v1',
      description="يک ای پی آی مخصوص اپلیکیشن فروشگاهی شما",
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
   generator_class= None
=======
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
>>>>>>> edb947b97584b34cbe74bc837c3a16415359efa5
)


urlpatterns = [
    path('api/admin/', admin.site.urls),
    path('api/account/', include("accounts.urls")),
    path('api/products/', include("products.urls")),
    path('api/cart/', include("cart.urls")),

    # YOUR PATTERNS
    # path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Optional UI:
    # path('', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
   path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
<<<<<<< HEAD
   path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
=======
   path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
>>>>>>> edb947b97584b34cbe74bc837c3a16415359efa5
   path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    # path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)