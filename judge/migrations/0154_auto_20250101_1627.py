# Generated by Django 3.2.25 on 2025-01-01 16:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('judge', '0153_auto_20241124_1513'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='data_rec',
            field=models.JSONField(default=list),
        ),
        migrations.AlterField(
            model_name='survey',
            name='algorithm',
            field=models.IntegerField(choices=[(14, 'Chưa từng học'), (15, 'Đã học cơ bản (sắp xếp, tìm kiếm, stack, queue)'), (16, 'Thành thạo (ứng dụng giải bài toán thực tế)')], default=None, null=True),
        ),
        migrations.AlterField(
            model_name='survey',
            name='contest',
            field=models.IntegerField(choices=[(17, 'Chưa bao giờ'), (18, 'Thỉnh thoảng'), (19, 'Thường xuyên')], default=None, null=True),
        ),
        migrations.AlterField(
            model_name='survey',
            name='experience',
            field=models.IntegerField(choices=[(6, 'Dưới 1 năm'), (7, '1-3 năm'), (8, 'Trên 3 năm')], default=None, null=True),
        ),
        migrations.AlterField(
            model_name='survey',
            name='hobby',
            field=models.IntegerField(choices=[(20, 'Tốc độ giải bài'), (21, 'Độ chính xác và tối ưu'), (22, 'Học được kiến thức mới'), (23, 'Tận hưởng quá trình thử nghiệm')], default=None, null=True),
        ),
        migrations.AlterField(
            model_name='survey',
            name='purpose',
            field=models.IntegerField(choices=[(9, 'Làm quen ngôn ngữ mới'), (10, 'Luyện tập kỹ năng')], default=None, null=True),
        ),
        migrations.AlterField(
            model_name='survey',
            name='skill_level',
            field=models.IntegerField(choices=[(11, 'Mới bắt đầu (Hiểu cơ bản các khái niệm)'), (12, 'Trung bình (Giải quyết được các bài toán cơ bản và trung cấp)'), (13, 'Nâng cao (Xây dựng được các dự án lớn, hiểu thuật toán phức tạp)')], default=None, null=True),
        ),
    ]
