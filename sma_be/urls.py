"""sma_be URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path
from sma_be.sectorservice import SectorAnalysis
from sma_be.sectorservice import HotSector
from sma_be.sectorservice import PredictTrend
from sma_be.common import UserManager

urlpatterns = [
    path('admin/', admin.site.urls),
    path("sectoranalysis.json/", SectorAnalysis.getHotSectorAnalysisInfor),
    path("hotsectorinfo.json/", HotSector.getHotSectorInfor),
    path("predictinfo.json/", PredictTrend.sendPredictData),
    path("login/", UserManager.checkUserInfo),
    path("register/", UserManager.register)
]
