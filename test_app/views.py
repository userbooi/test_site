from django.shortcuts import render, redirect
from .models import Topics, Entry
from .forms import TopicForm, EntryForm
from django.contrib.auth.decorators import login_required
from django.http import Http404

# Create your views here.
def index(request):
    return render(request, 'test_app/index.html')

@login_required
def topics(request):
    topics = Topics.objects.filter(owner=request.user).order_by('date_added')
    context = {'topics': topics}
    return render(request, "test_app/topics.html", context)

@login_required
def topic(request, topic_id):
    topic = Topics.objects.get(id=topic_id)
    if topic.owner != request.user:
        raise Http404
    entries = topic.entry_set.order_by('-date_added')
    context = {"topic":topic, "entries":entries}
    return render(request, "test_app/topic.html", context)

@login_required
def new_topic(request):
    if request.method != 'POST':
        form = TopicForm()
    else:
        form = TopicForm(data=request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return redirect("test_app:topics")

    context = {'form':form}
    return render(request, 'test_app/new_topic.html', context)

@login_required
def new_entry(request, topic_id):
    topic = Topics.objects.get(id=topic_id)

    if request.method != 'POST':
        form = EntryForm()
    else:
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return redirect("test_app:topic", topic_id=topic_id)

    context={"form":form, "topic":topic}
    return render(request, 'test_app/new_entry.html', context)

@login_required
def edit_entry(request, entry_id):
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    if topic.owner != request.user:
        raise Http404

    if request.method != "POST":
        form = EntryForm(instance=entry)
    else:
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect("test_app:topic", topic_id=topic.id)

    context = {'entry':entry, 'topic':topic, 'form':form}
    return render(request, "test_app/edit_entry.html", context)
