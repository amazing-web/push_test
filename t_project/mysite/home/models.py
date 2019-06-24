from django import forms
from django.db import models

from modelcluster.fields import ParentalKey, ParentalManyToManyField
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase

from wagtail.core.models import Page, Orderable
from wagtail.core.fields import RichTextField, StreamField
from wagtail.admin.edit_handlers import (
    FieldPanel, InlinePanel, MultiFieldPanel,
    PageChooserPanel, StreamFieldPanel, FieldRowPanel
)
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index

from wagtail.snippets.models import register_snippet

from wagtail.images.models import Image

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


from wagtail.images.blocks import ImageChooserBlock
from wagtail.core import blocks

from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField


class HomePage(Page):
    intro = models.CharField(max_length=250)
    author = ParentalManyToManyField('home.Authors', blank=True)
    form_page = models.ForeignKey(
        'wagtailcore.Page',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='embedded_form_page',
        help_text='Select a Form that will be embedded on this page.'
    )

    content_panels = Page.content_panels + [
        FieldPanel('intro'),
        FieldPanel('author', widget=forms.CheckboxSelectMultiple),
        PageChooserPanel('form_page', ['home.FormPage'])
    ]

    def get_context(self, request):
        context = super().get_context(request)
        all_blogpages = BlogPage.objects.live().order_by('-first_published_at')
        paginator = Paginator(all_blogpages, 5)
        page = request.GET.get('page')
        try:
            blogpages = paginator.page(page)
        except PageNotAnInteger:
            blogpages = paginator.page(1)
        except EmptyPage:
            blogpages = paginator.page(paginator.num_pages)
        context['blogpages'] = blogpages
        context['all_blogpages'] = all_blogpages
        categories = CategoryIndex.objects.all
        context['categories'] = categories
        advertisements = Advertisement.objects.all
        context['advertisements'] = advertisements
        if self.form_page:
            form_page = self.form_page.specific
            form = form_page.get_form(page=form_page, user=request.user)
            context['form'] = form
        return context

class BlogPage(Page):
    date = models.DateField("Post date")
    intro = models.CharField(max_length=250)
    topics = ParentalManyToManyField('home.Topic', blank=True)
    categories = ParentalManyToManyField('home.Category', blank=True)
    body = StreamField([
        ('paragraph', blocks.RichTextBlock(icon='edit')),
        ('h2', blocks.CharBlock(icon='title')),
        ('h3', blocks.CharBlock(icon='title')),
        ('comment', blocks.RichTextBlock(icon='openquote')),
        ('image', ImageChooserBlock()),
        ('html', blocks.RawHTMLBlock()),
    ])
    cover = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    top_num = models.CharField(
        max_length=1,
        blank=True,
    )

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('body'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('intro'),
        StreamFieldPanel('body'),
        MultiFieldPanel([
            FieldPanel('date'),
            FieldPanel('topics', widget=forms.CheckboxSelectMultiple),
            FieldPanel('top_num'),
            FieldPanel('categories', widget=forms.CheckboxSelectMultiple),
            ImageChooserPanel('cover'),
        ], heading='Information'),
    ]

    def get_context(self, request):
        context = super().get_context(request)
        parent = HomePage.objects.specific().all()
        advertisements = Advertisement.objects.all()
        all_blogpages = BlogPage.objects.live().order_by('-first_published_at')
        categories = CategoryIndex.objects.all
        form = FormPage.objects.all()
        context['parent'] = parent
        context['advertisements'] = advertisements
        context['all_blogpages'] = all_blogpages
        context['categories'] = categories
        context['form'] = form
        return context

@register_snippet
class Authors(models.Model):
    name = models.CharField(max_length=30, blank=True)
    icon = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    intro = models.CharField(max_length=250, blank=True)

    panels = [
        FieldPanel('name'),
        ImageChooserPanel('icon'),
        FieldPanel('intro'),
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'authors'

@register_snippet
class Topic(models.Model):
    name = models.CharField(max_length=255)

    panels = [
        FieldPanel('name'),
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'topics'

@register_snippet
class Category(models.Model):
    name = models.CharField(max_length=255)

    panels = [
        FieldPanel('name'),
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'categories'

class CategoryIndex(Page):
    def children(self):
        return self.get_children()
    def get_context(self, request):
        context = super().get_context(request)
        parent = HomePage.objects.specific().all()
        advertisements = Advertisement.objects.all()
        all_blogpages = BlogPage.objects.live().order_by('-first_published_at')
        categories = self.get_children().specific()
        form = FormPage.objects.all()
        context['parent'] = parent
        context['advertisements'] = advertisements
        context['all_blogpages'] = all_blogpages
        context['categories'] = categories
        context['form'] = form
        return context

class Shimanto(Page):
    def get_context(self, request):
        context = super().get_context(request)
        all_blogpages = BlogPage.objects.filter(categories__name='Shimanto').live().order_by('-first_published_at')
        paginator = Paginator(all_blogpages, 5)
        page = request.GET.get('page')
        try:
            blogpages = paginator.page(page)
        except PageNotAnInteger:
            blogpages = paginator.page(1)
        except EmptyPage:
            blogpages = paginator.page(paginator.num_pages)
        context['blogpages'] = blogpages
        parent = HomePage.objects.specific().all()
        advertisements = Advertisement.objects.all()
        all_blogpages = BlogPage.objects.live().order_by('-first_published_at')
        categories = CategoryIndex.objects.all
        form = FormPage.objects.all()
        context['parent'] = parent
        context['advertisements'] = advertisements
        context['all_blogpages'] = all_blogpages
        context['categories'] = categories
        context['form'] = form
        return context

class Nagara(Page):
    def get_context(self, request):
        context = super().get_context(request)
        all_blogpages = BlogPage.objects.filter(categories__name='Nagara').live().order_by('-first_published_at')
        paginator = Paginator(all_blogpages, 5)
        page = request.GET.get('page')
        try:
            blogpages = paginator.page(page)
        except PageNotAnInteger:
            blogpages = paginator.page(1)
        except EmptyPage:
            blogpages = paginator.page(paginator.num_pages)
        context['blogpages'] = blogpages
        parent = HomePage.objects.specific().all()
        advertisements = Advertisement.objects.all()
        all_blogpages = BlogPage.objects.live().order_by('-first_published_at')
        categories = CategoryIndex.objects.all
        form = FormPage.objects.all()
        context['parent'] = parent
        context['advertisements'] = advertisements
        context['all_blogpages'] = all_blogpages
        context['categories'] = categories
        context['form'] = form
        return context

class Kakita(Page):
    def get_context(self, request):
        context = super().get_context(request)
        all_blogpages = BlogPage.objects.filter(categories__name='Kakita').live().order_by('-first_published_at')
        paginator = Paginator(all_blogpages, 5)
        page = request.GET.get('page')
        try:
            blogpages = paginator.page(page)
        except PageNotAnInteger:
            blogpages = paginator.page(1)
        except EmptyPage:
            blogpages = paginator.page(paginator.num_pages)
        context['blogpages'] = blogpages
        parent = HomePage.objects.specific().all()
        advertisements = Advertisement.objects.all()
        all_blogpages = BlogPage.objects.live().order_by('-first_published_at')
        categories = CategoryIndex.objects.all
        form = FormPage.objects.all()
        context['parent'] = parent
        context['advertisements'] = advertisements
        context['all_blogpages'] = all_blogpages
        context['categories'] = categories
        context['form'] = form
        return context

@register_snippet
class Advertisement(models.Model):
    name = models.CharField(max_length=30, blank=True)
    url = StreamField([
        ('html', blocks.RawHTMLBlock())
    ])

    panels = [
        FieldPanel('name'),
        StreamFieldPanel('url')
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'advertisements'

class FormField(AbstractFormField):
    page = ParentalKey('FormPage', on_delete=models.CASCADE, related_name='form_fields')

class FormPage(AbstractEmailForm):
    intro = RichTextField(blank=True)
    thank_you_text = RichTextField(blank=True)

    content_panels = AbstractEmailForm.content_panels + [
        FieldPanel('intro', classname="full"),
        InlinePanel('form_fields', label="Form fields"),
        FieldPanel('thank_you_text', classname="full"),
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('from_address', classname="col6"),
                FieldPanel('to_address', classname="col6"),
            ]),
            FieldPanel('subject'),
        ], "Email"),
    ]

    def get_context(self, request):
        context = super().get_context(request)
        parent = HomePage.objects.specific().all()
        advertisements = Advertisement.objects.all()
        all_blogpages = BlogPage.objects.live().order_by('-first_published_at')
        categories = CategoryIndex.objects.all
        context['parent'] = parent
        context['advertisements'] = advertisements
        context['all_blogpages'] = all_blogpages
        context['categories'] = categories
        return context
