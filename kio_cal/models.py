# -*- coding: utf-8 -*-

from datetime import datetime
from django.core.urlresolvers import reverse
from django.db import models
from django.contrib.auth.models import User
from sentry.helpers import cached_property

from colorfield.fields import ColorField

from shared.utils import upload_to,int2roman,get_admin_url

class ReadyManager(models.Manager):
    def public(self):
        return super(ReadyManager,self).get_query_set().\
            filter(is_ready=True)

class Rubric(models.Model):
    '''Рубрика журнала КИО'''

    authors = models.ManyToManyField(User,verbose_name=u'Редакторы')
    title =  models.CharField(u'Название',max_length=256)
    color = ColorField(u'Цвет фона для рубрики',
                              help_text=u'Подбирайте как можно более\
                               блёклый цвет')

    #TODO: link
    #@models.permalink
    def get_absolute_url(self):
        return ' '

    def get_rss_url(self):
        return reverse('rubric_rss_feed',args=(self.pk,))

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = u'рубрика'
        verbose_name_plural = u'рубрики'

class Article(models.Model):
    '''Статья журнала КИО'''

    authors = models.ManyToManyField(User,verbose_name=u'Авторы')
    rubric = models.ForeignKey(Rubric,verbose_name=u'Рубрика')
    title = models.CharField(u'Заголовок статьи',max_length=256)
    body = models.TextField(u'Текст статьи')
    main_image = models.ImageField(u'Картинка для главной страницы',
                                   upload_to=upload_to('uploads/article/'),
                                   null=True,blank=True)
    is_ready = models.BooleanField(u'Закончена')
    created_dt = models.DateField(u'дата добавления',auto_now_add=True)
    modified_dt = models.DateField(u'дата обновления',auto_now=True)
    status_db = models.CharField(u'Статус',max_length=24,
                                 editable=False,default=u'в процессе')

    objects = ReadyManager()

    def is_published(self):
        for relc in self.releases.all():
            if relc.is_published():
                return True
        return False

    def is_published_display(self):
        if self.releases.exists():
            return u', '.join([r.title for r in self.releases.all()])
        else:
            return u'-нет-'
    is_published_display.short_description = u'выпуски'

    def status(self):
        # опубликована?
        if self.is_published():
            return 'published'
        # запланирована публикация?
        if self.releases.exists():
            return 'approved'
        # автор думает что готово?
        if self.is_ready:
            return 'done'
        #статья в процессе
        return 'progress'

    @models.permalink
    def get_absolute_url(self):
        return ('article_full',(self.pk,))

    def get_admin_url(self):
        return get_admin_url(self)

    def __unicode__(self):
        return self.title

    def save(self, force_insert=False, force_update=False, using=None):
        ru_names = {
             'published': u'опубликована',
             'approved': u'в выпуске',
             'done': u'готова',
             'progress': u'в процессе'
         }
        if self.pk:
            self.status_db = ru_names.get(self.status(),'?')
        else:
            self.status_db = ru_names.get('progress','?')
        return super(Article, self).save(force_insert, force_update, using)

    class Meta:
        verbose_name = u'cтатья'
        verbose_name_plural = u'cтатьи'
        ordering = ('-created_dt',)


class ReleaseManager(ReadyManager):
    def public(self):
        return super(ReleaseManager,self).public().\
            filter(publication_ts__lt=datetime.now())

class Release(models.Model):
    articles = models.ManyToManyField(Article,
                                     through='ReleaseArticleMembership',
                                     verbose_name=u'статьи выпуска',
                                     related_name='releases')
    publication_ts = models.DateTimeField(u'Дата и время публикации',
                            help_text=u'точное время с которого выпуск\
                            доступен читателям')
    is_ready = models.BooleanField(u'Готов к публикации',
                            help_text=u'необходимо отметить при публикации')

    objects = ReleaseManager()


    def articles_ordered(self):
        return self.articles.order_by('releasearticlemembership__order')

    def is_published(self):
        return (self.is_ready and self.publication_ts<datetime.now()\
                and True) or False
    is_published.short_description = u'опубликован'

    def before(self):
        return Release.objects.public()\
                            .filter(publication_ts__lt=self.publication_ts)\
                            .order_by('-publication_ts')

    def after(self):
        return Release.objects.public()\
                        .filter(publication_ts__gt=self.publication_ts)\
                        .order_by('publication_ts')

    @models.permalink
    def get_absolute_url(self):
        #for public
        if self.is_published():
            #first check that is only release in month or not
            count = None
            if Release.objects.filter(
                                publication_ts__year=self.publication_ts.year,
                                publication_ts__month=self.publication_ts.month,
                                is_ready=True).exclude(pk=self.pk).exists():
                for (i,release) in  enumerate(Release.objects.filter(
                                publication_ts__year=self.publication_ts.year,
                                publication_ts__month=self.publication_ts.month,
                                is_ready=True)):
                    if release.pk == self.pk:
                        count = i

            coords = {  'year':self.publication_ts.year,
                        'month':self.publication_ts.month,}

            #if more than one release, then add number
            if count:
                coords['count'] = count

            return ('release_by_date', [], coords)
        #for admin and etc
        else:
            return ('release', [self.pk])

    def save(self, force_insert=False, force_update=False, using=None):
        res = super(Release, self).save(force_insert, force_update, using)
        # update statuses
        for a in self.articles.all():
            a.save()
        return res

    @cached_property
    def title(self):
        MONTHS = (
            u'январь',
            u'февраль',
            u'март',
            u'апрель',
            u'май',
            u'июнь',
            u'июль',
            u'август',
            u'сентябрь',
            u'октябрь',
            u'ноябрь',
            u'декабрь',
        )

        #check that is only one release in this month
        postfix = ''
        if Release.objects.public().filter(
                            publication_ts__year=self.publication_ts.year,
                            publication_ts__month=self.publication_ts.month)\
                            .exclude(pk=self.pk).exists():
            for (i,release) in  enumerate(Release.objects.public().filter(
                            publication_ts__year=self.publication_ts.year,
                            publication_ts__month=self.publication_ts.month)
                            .order_by('publication_ts')):
                if release.pk == self.pk:
                    postfix = u' (часть %s)'%int2roman(i+1)

        return u'%s %s %s'%(MONTHS[self.publication_ts.month-1],
                         self.publication_ts.year,postfix)

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = u'выпуск'
        verbose_name_plural = u'выпуски'
        ordering = ('-publication_ts',)



class ReleaseArticleMembership(models.Model):
    release = models.ForeignKey(Release)
    article = models.ForeignKey(Article)
    order = models.PositiveSmallIntegerField()

    def __init__(self, *args, **kwargs):
#        self.order = ReleaseArticleMembership.objects\
#                    .filter(release=self.release,
#                            article = self.article)\
#                    .count()+1
        super(ReleaseArticleMembership, self).__init__(*args, **kwargs)

    class Meta:
        ordering = ('release__id','order','id')
        verbose_name = u'cтатья'
        verbose_name_plural = u'cтатьи'