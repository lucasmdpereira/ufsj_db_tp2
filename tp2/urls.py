from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from v1 import views

router = DefaultRouter(trailing_slash=False)

router.register(r"estabelecimentos", views.EstabelecimentoView, "estabelecimentos")
router.register(r"comentarios", views.ComentarioViewSet, "comentarios")
router.register(r"respostas", views.RespostaViewSet, "respostas")
router.register(r"resumos-de-avaliacoes", views.ResumoDeAvaliacoesViewSet, "resumos-de-avaliacoes")
router.register(r"tags", views.TagViewSet, "tags")
router.register(r"estabelecimentos-tags", views.EstabelecimentoTagView, "estabelecimentos-tags")


urlpatterns = [
    path("v1/", include(router.urls)),
    path("v1/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("v1/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("v1/token/verify/", TokenVerifyView.as_view(), name="token_verify"),
]

