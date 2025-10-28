from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages
from .models import RecordEntry, RecordImage
from .forms import RecordEntryForm


def home(request):
    """
    Главная страница - отображает одобренные рекорды с фильтрацией и пагинацией
    """
    # Получаем только одобренные рекорды
    records = RecordEntry.objects.filter(is_approved=True)
    
    # Фильтр по названию
    title_filter = request.GET.get('title', '')
    if title_filter:
        records = records.filter(title__icontains=title_filter)
    
    # Сортировка по дате
    sort_order = request.GET.get('sort', 'desc')
    if sort_order == 'asc':
        records = records.order_by('created_at')
    else:
        records = records.order_by('-created_at')
    
    # Пагинация - 10 рекордов на страницу
    paginator = Paginator(records, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'title_filter': title_filter,
        'sort_order': sort_order,
    }
    
    return render(request, 'records/home.html', context)


def create_record(request):
    """
    Страница добавления рекорда - GET для отображения формы, POST для создания
    """
    if request.method == 'POST':
        form = RecordEntryForm(request.POST, request.FILES)
        if form.is_valid():
            # Сохраняем рекорд без изображений для поста
            record = form.save(commit=False)
            record.save()
            
            # Обрабатываем дополнительные изображения
            images = request.FILES.getlist('images')
            for image in images:
                record_image = RecordImage.objects.create(image=image)
                record.images.add(record_image)
            
            messages.success(
                request, 
                'Ваш рекорд успешно добавлен и будет рассмотрен администратором в ближайшее время.'
            )
            
            # Очищаем форму после успешной отправки
            form = RecordEntryForm()
    else:
        form = RecordEntryForm()
    
    return render(request, 'records/create_record.html', {'form': form})


def record_detail(request, record_id):
    """
    Страница отдельного рекорда
    """
    record = get_object_or_404(RecordEntry, id=record_id)
    
    context = {
        'record': record,
    }
    
    return render(request, 'records/record_detail.html', context)
