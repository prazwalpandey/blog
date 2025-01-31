from django.shortcuts import render, get_object_or_404
from .models import Post
# from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView, DetailView, FormView
from  django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from .forms import SearchForm
# CommentForm, EmailPostForm,
from django.http import JsonResponse
from django.core.paginator import Paginator


class PostListView(ListView):
    '''
    Alternative post List View
    '''
    # context_object_name = 'posts'
    # paginate_by = 5
    # template_name = 'blog/post/list.html'

    # def get_queryset(self):
    #     return Post.published.all()
    # model = Post
    queryset = Post.published.all()
    context_object_name = "posts"
    paginate_by = 4
    template_name = "blog/post/list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["pinned_posts"] = Post.published.filter(pinned=True).order_by("-publish")
        context["most_liked_posts"] = Post.published.order_by("-likes")[:5]
        return context


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post/detail.html'
    context_object_name = "post"
    form = SearchForm()

    def get_object(self, queryset=None):
        return get_object_or_404(
            Post,
            # self.form,
            status=Post.Status.PUBLISHED,
            slug=self.kwargs["post"],
            publish__year=self.kwargs["year"],
            publish__month=self.kwargs["month"],
            publish__day=self.kwargs["day"],
        )


class PostSearchView(FormView):
    template_name = "blog/post/search.html"
    form_class = SearchForm

    def get(self, request, *args, **kwargs):
        form = self.get_form()
        query = None
        results = []

        if 'query' in request.GET:
            form = self.form_class(request.GET)
            if form.is_valid():
                query = form.cleaned_data['query']
                search_query = SearchQuery(query)
                results = (
                    Post.published.annotate(
                        search=SearchVector('title', 'body'),
                        rank=SearchRank(SearchVector('title', 'body'), 
                                        search_query)
                    )
                    .filter(search=query)
                    .order_by('-rank')
                )

        return render(
            request,
            self.template_name,
            {'form': form, 'query': query, 'results': results}
        )


def like_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.likes += 1
    post.save()
    return JsonResponse({"likes": post.likes})