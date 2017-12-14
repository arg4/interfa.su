from django.shortcuts import render
from django.db.models import Count
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from .models import Article, Comment, Draft
from .forms import CommentForm, DraftFormLink, DraftFormEditorial, DraftFormTutorial, ArticleFormLink, ArticleFormEditorial, ArticleFormTutorial
from django.contrib.auth.decorators import login_required, user_passes_test

# Security views access to restricted areas of the site.
def not_in_author_group(user):
    if user:
        return user.groups.filter(name='Author').exists()
    return False

def not_in_mod_group(user):
    if user:
        return user.groups.filter(name='Mod').exists()
    return False

# Create your views here.
def index(request, page_id=1, filter_mode='n'):
    """IW_app Index page"""

    if filter_mode == 'p':# list articles by comment_set length
        articles_list = Article.objects.annotate(num_comments=Count('comment')).order_by('-num_comments')

    elif filter_mode == 'c':# list articles with only original content. ie tutorial and editorial type articles.
        articles_list = Article.objects.all().exclude(article_type = "LI")
    elif filter_mode == 'o': # list oldest articles first
        articles_list = Article.objects.all().order_by("pk")
    else: # in most cases this should be n (newest items first)
        filter_mode = 'n'
        articles_list = Article.objects.all().order_by("-pk")

    paginator = Paginator(articles_list, 10) # Show 10 Articles per page

    try:
        articles = paginator.page(page_id)
    except PageNotAnInteger:
        articles = paginator.page(1)
    except EmptyPage:
        articles = paginator.page(paginator.num_pages)

    context = {'articles': articles, 'filter_mode':filter_mode}

    return render(request, 'iw_app/index.html', context)
    #articles = Article.objects.all().order_by("-pk")
    #context = {'articles': articles}
    #return render(request, 'iw_app/index.html', context)



def article(request, article_id):
    """ Return a given article from a url """
    try:
        article = Article.objects.get(id=article_id)
    except Article.DoesNotExist:
        raise Http404("Nothing here")

    if request.method != 'POST':
        # No data submitted return article and blank form
        form = CommentForm()
    else:
        # POST data submitted; process data.
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.comment_on = article
            if request.user.is_authenticated():
                new_comment.comment_owner = request.user
            if 'anon_post' in request.POST:
                new_comment.commented_anonymously = True
            new_comment.save()
            return HttpResponseRedirect(reverse('iw_app:article',args=[article_id]))

    form = CommentForm()
    comments = article.comment_set.order_by("date_created")
    context = {'article': article, 'comments': comments, 'form': form, request:'request'}
    return render(request, 'iw_app/article.html', context)



def about_contact(request):
    """ Return a simple about page that describes the site and provides contact info for the admins."""
    context = {request:'request'}
    return render(request, 'iw_app/about.html', context)


@login_required
@user_passes_test(not_in_mod_group, login_url='/users/login/', redirect_field_name=None)
def content_moderation(request):
    """
    View flagged posts by post w/ the most flags provide interface
    to delete those posts.
    """


@login_required
@user_passes_test(not_in_author_group, login_url='/users/login/', redirect_field_name=None)
def article_staging_all(request):
    """
    Show all articles that are currently being considered, provide a comment
    thread for each article for authors to talk on, and possible revision history
    of each article. As well as voting.
    """

    drafts = Draft.objects.all().exclude(make_public = False).order_by('-pk')
    my_drafts = Draft.objects.all().filter(name_author=request.user).order_by('-pk')
    my_articles = Article.objects.all().filter(name_author=request.user).order_by('-pk')

    if request.method == 'POST':
        if request.POST.get('make_public_swap'):
            draft_id = int(request.POST.get('make_public_swap'))
            draft = Draft.objects.get(id=draft_id)
            if draft not in my_drafts:
                return  HttpResponseRedirect(reverse('iw_app:staging_all'))
            if draft.make_public == True:
                draft.make_public = False
                draft.save()
            else:
                draft.make_public = True
                draft.save()
        elif request.POST.get('vote_article'):
            draft_id = int(request.POST.get('vote_article'))
            draft = Draft.objects.get(id=draft_id)
            #TODO add a condition that prevents authors from boosting their own articles.
            if Draft.objects.all().filter(id=draft_id, voters=request.user).exists():
                return  HttpResponseRedirect(reverse('iw_app:staging_all'))
                #If user has already voted, redirected to draft page.
            else:
                #print('vote could be acceptable')
                draft.voters.add(request.user)
                draft.draft_vote += 1
                draft.save()
                if draft.draft_vote >= 2: # This condition determines how many votes a draft needs to succeed.
                    new_article_from_draft(draft)
        return  HttpResponseRedirect(reverse('iw_app:staging_all'))

    context = { 'request' :request ,
                'drafts' :drafts ,
                'my_drafts':my_drafts,
                'my_articles':my_articles,
                }
    return render(request, 'iw_app/staging_area.html', context)



def new_article_from_draft(draft):
    """
    If a draft gains enough votes, create a new article from that draft
    """
    new_article = Article(  article_name = draft.article_name,
                            article_external_url = draft.article_external_url,
                            #name_author = draft.name_author,
                            article_description = draft.article_description,
                            article_body_text = draft.article_body_text,
                            article_caption_styles = draft.article_caption_styles,
                            article_type = draft.article_type,
                            )

    new_article.save()
    old_authors = draft.name_author.all()
    new_article.name_author = old_authors
    new_article.save()
    draft.delete()
    print(old_authors)
    print(new_article.id)


@login_required
@user_passes_test(not_in_author_group, login_url='/users/login/', redirect_field_name=None)
def article_staging_individual(request, staged_article):
    """
    View the article in a template and vote on the article
    """
    article = Draft.objects.get(id=staged_article)
    context = { 'request':request,
                'article': article
                }
    return render(request, 'iw_app/staging_individual.html', context)


@login_required
@user_passes_test(not_in_author_group, login_url='/users/login/', redirect_field_name=None)
def new_draft(request, filter_m ='l'):
    """
    Redo code pertaining to the creation of new drafts
    """
    # Determine what kind of draft is being created.
    if filter_m == 'e':
        draft_type = 'ED'
    elif filter_m == 't':
        draft_type = 'TU'
    else:
        draft_type = 'LI'
    # If request is not = to post return the right kind of form.
    if request.method != 'POST':
        if draft_type == 'ED':
            form = DraftFormEditorial(request.user.id)
        elif draft_type == 'TU':
            form = DraftFormTutorial(request.user.id)
        else:
            form = DraftFormLink(request.user.id)
    # If request IS post. validate form.
    else:
        if draft_type == 'ED':
            form = DraftFormEditorial(request.user.id, request.POST)
        elif draft_type == 'TU':
            form = DraftFormTutorial(request.user.id, request.POST)
        else:
            form = DraftFormLink(request.user.id, request.POST)
        # Check the validity of the form and fill fields if valid.
        if form.is_valid():
            new_draft = form.save(commit=False)
            new_draft.article_type = draft_type
            new_draft.save()
            # This is super important
            form.save_m2m()
            new_draft.name_author.add(request.user)
            # Redirect back to staging area.
            return HttpResponseRedirect(reverse('iw_app:staging_all'))

    context = {'form': form, 'filter_m': filter_m}
    return render(request, 'iw_app/edit_article_draft.html', context)


@login_required
@user_passes_test(not_in_author_group, login_url='/users/login/', redirect_field_name=None)
def edit_draft(request, draft_id):
    """
    This is the interface where the author can edit an articles draft.
    """
    draft = Draft.objects.get(id=draft_id)

    if request.method != 'POST':
        if draft.article_type == 'LI':
            form = DraftFormLink(request.user.id, instance=draft)
        elif draft.article_type == 'ED':
            form = DraftFormEditorial(request.user.id, instance=draft)
        else:
            form = DraftFormTutorial(request.user.id, instance=draft)
    else:
        if draft.article_type == 'LI':
            form = DraftFormLink(request.user.id, instance=draft, data=request.POST)
        elif draft.article_type == 'ED':
            form = DraftFormEditorial(request.user.id, instance=draft, data=request.POST)
        else:
            form = DraftFormTutorial(request.user.id, instance=draft, data=request.POST)
        #Check form validity
        if form.is_valid():
            form.save()
            draft.name_author.add(request.user)
            if 'return_and_preview' in request.POST:
                return HttpResponseRedirect(reverse('iw_app:staging_indv', args=[draft_id]))
            elif 'delete_this_thing' in request.POST:
                Draft.objects.get(id=draft_id).delete()
            return HttpResponseRedirect(reverse('iw_app:staging_all'))

    context = {'form': form, 'draft':draft}
    return render(request, 'iw_app/edit_article_draft.html', context)


@login_required
@user_passes_test(not_in_author_group, login_url='/users/login/', redirect_field_name=None)
def edit_article(request, article_id):
    """
    This interface allows the author to edit a complete article
    """
    article = Article.objects.get(id=article_id)

    if request.method != 'POST':
        if article.article_type == 'LI':
            form = ArticleFormLink(request.user.id, instance=article)
        elif article.article_type == 'ED':
            form = ArticleFormEditorial(request.user.id, instance=article)
        else:
            form = ArticleFormTutorial(request.user.id, instance=article)
    else:
        if article.article_type == 'LI':
            form = ArticleFormLink(request.user.id, instance=article, data=request.POST)
        elif article.article_type == 'ED':
            form = ArticleFormEditorial(request.user.id, instance=article, data=request.POST)
        else:
            form = ArticleFormTutorial(request.user.id, instance=article, data=request.POST)
        #Check form validity
        if form.is_valid():
            form.save()
            article.name_author.add(request.user)
            if 'return_and_preview' in request.POST:
                return HttpResponseRedirect(reverse('iw_app:article', args=[article_id]))
            return HttpResponseRedirect(reverse('iw_app:staging_all'))

    context = {'form': form, 'article':article}
    return render(request, 'iw_app/edit_article_draft.html', context)
