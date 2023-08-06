from django.db import models


class Portfolio(models.Model):
    title = models.CharField('제목', max_length=20)
    subtitle = models.CharField('부제목', max_length=40)
    filter = models.ForeignKey(
        'Category',
        related_name='category',
        on_delete=models.PROTECT,
    )
    description = models.TextField('세부 설명', null=True, blank=True)
    image1 = models.ImageField(upload_to=f'images/portfolio/', null=True,
                               help_text="각 이미지 비율이(3x5, 4x5) 동일한 것이 보기 좋습니다.")
    image2 = models.ImageField(upload_to=f'images/portfolio/', null=True, blank=True)
    image3 = models.ImageField(upload_to=f'images/portfolio/', null=True, blank=True)
    image4 = models.ImageField(upload_to=f'images/portfolio/', null=True, blank=True)
    image5 = models.ImageField(upload_to=f'images/portfolio/', null=True, blank=True)
    url = models.URLField('참고링크', blank=True, null=True, help_text="공란 가능")

    def __str__(self):
        return self.title


class Category(models.Model):
    filter = models.CharField('카테고리', max_length=20)

    def __str__(self):
        return self.filter

