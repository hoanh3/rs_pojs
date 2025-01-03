# Generated by Django 3.2.25 on 2024-11-24 15:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('judge', '0152_auto_20241122_0943'),
    ]

    operations = [
        migrations.AddField(
            model_name='survey',
            name='algorithm',
            field=models.IntegerField(choices=[(1, 'Chưa từng học'), (2, 'Đã học cơ bản (sắp xếp, tìm kiếm, stack, queue)'), (3, 'Thành thạo (ứng dụng giải bài toán thực tế)')], default=None, null=True),
        ),
        migrations.AddField(
            model_name='survey',
            name='contest',
            field=models.IntegerField(choices=[(1, 'Chưa bao giờ'), (2, 'Thỉnh thoảng'), (3, 'Thường xuyên')], default=None, null=True),
        ),
        migrations.AddField(
            model_name='survey',
            name='hobby',
            field=models.IntegerField(choices=[(1, 'Tốc độ giải bài'), (2, 'Độ chính xác và tối ưu'), (3, 'Học được kiến thức mới'), (4, 'Tận hưởng quá trình thử nghiệm')], default=None, null=True),
        ),
        migrations.AddField(
            model_name='survey',
            name='skill_level',
            field=models.IntegerField(choices=[(1, 'Mới bắt đầu (Hiểu cơ bản các khái niệm)'), (2, 'Trung bình (Giải quyết được các bài toán cơ bản và trung cấp)'), (3, 'Nâng cao (Xây dựng được các dự án lớn, hiểu thuật toán phức tạp)')], default=None, null=True),
        ),
        migrations.AlterField(
            model_name='survey',
            name='experience',
            field=models.IntegerField(choices=[(1, 'Dưới 1 năm'), (2, '1-3 năm'), (3, 'Trên 3 năm')], default=None, null=True),
        ),
        migrations.AlterField(
            model_name='survey',
            name='language',
            field=models.IntegerField(choices=[(1, 'Python'), (2, 'JavaScript'), (3, 'Java'), (4, 'C++'), (5, 'Khác')], default=None, null=True),
        ),
        migrations.AlterField(
            model_name='survey',
            name='purpose',
            field=models.IntegerField(choices=[(1, 'Làm quen ngôn ngữ mới'), (2, 'Luyện tập kỹ năng')], default=None, null=True),
        ),
    ]
