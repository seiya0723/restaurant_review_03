from django.shortcuts import render,redirect
from django.views import View

from .models import Restaurant,Review,Category
from .forms import RestaurantForm,ReviewForm,CategoryForm

class IndexView(View):

    def get(self, request, *args, **kwargs):
        
        #TODO:飲食店一覧を表示させる(新しい順に)
        context                 = {}
        context["restaurants"]  = Restaurant.objects.order_by("-dt")

        return render(request,"restaurant/index.html",context)

index   = IndexView.as_view()

class SingleView(View):

    def get(self, request, pk, *args, **kwargs):

        #TODO:飲食店に投稿されたレビューを表示
        context                 = {}
        #単一のモデルオブジェクトを手に入れる。これはテンプレートでforループを行う必要はない。
        context["restaurant"]   = Restaurant.objects.filter(id=pk).first()
        context["reviews"]      = Review.objects.filter(restaurant=pk).order_by("-dt")

        return render(request,"restaurant/single.html",context)

    def post(self, request, pk, *args, **kwargs):

        #TODO:飲食店にレビューを投稿

        #リクエストオブジェクトに対象の店舗のidをセットする必要がある
        #だが、リクエストオブジェクトは書き換え不可能なデータである。
        #そのため、コピーを作って対象の店舗idをセットし、バリデーションする。


        copied                  = request.POST.copy()
        copied["restaurant"]    = pk

        form    = ReviewForm(copied)

        if form.is_valid():
            print("バリデーションOK")
            form.save()
        else:
            print("バリデーションNG")

        #リダイレクトする時は対象のidを指定する。
        return redirect("restaurant:single", pk )

single  = SingleView.as_view()

