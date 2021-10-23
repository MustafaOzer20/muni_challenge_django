from rest_framework import serializers
from book.models import Author, Publisher, Category, Comment, Book

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ('__all__')
    
    def create(self, validated_data):
        author = validated_data['author']
        publisher = validated_data['publisher']
        category = validated_data['category']
        old_author = Author.objects.filter(full_name=author).first()
        old_publisher = Publisher.objects.filter(name=publisher).first()
        old_category = Category.objects.filter(name=category).first()
        if author != str(old_author):
            new_author = Author(full_name=author)
            new_author.save()

        if publisher != str(old_publisher):
            new_publisher = Publisher(name=publisher)
            new_publisher.save()

        if category != str(old_category):
            new_category = Category(name=category)
            new_category.save()

        instance = self.Meta.model(**validated_data)
        instance.save()
        return instance

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('__all__')