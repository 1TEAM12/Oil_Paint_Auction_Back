# rest_framework
from rest_framework import serializers

# painting
from paintings.models import Painting
from paintings.styler import painting_styler


# 이미지 스타일러 serializer
class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Painting
        fields = (
            "id",
            "style",
            "before_image",
        )

    def create(self, validated_data):
        style_no = validated_data["style"]
        before_image = validated_data["before_image"]

        painting = Painting(style=style_no, before_image=before_image)
        painting.save()

        return painting


# 유화 생성 serializer
class PaintingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Painting
        fields = (
            "title",
            "content",
            "owner",
            "author",
            "after_image",
        )
        extra_kwargs = {
            "title": {
                "error_messages": {
                    "required": "제목을 입력해주세요",
                    "blank": "제목을 입력해주세요",
                }
            },
            "content": {
                "error_messages": {
                    "required": "내용을 입력해주세요.",
                    "blank": "내용을 입력해주세요.",
                }
            },
        }

    def update(self, instance, validated_data):
        instance.title = validated_data.get("title", instance.title)
        instance.content = validated_data.get("content", instance.content)
        instance.owner = validated_data.get("user_id", validated_data["owner"])
        instance.author = validated_data.get("user_id", validated_data["author"])
        instance.after_image = painting_styler(instance.before_image, instance.style)

        instance.save()

        return instance


# 유화 상세 serializer
class PaintingDetailSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    owner = serializers.SerializerMethodField()
    owner_profile_image = serializers.SerializerMethodField()
    author_profile_image = serializers.SerializerMethodField()

    def get_author(self, obj):
        return obj.author.nickname

    def get_owner(self, obj):
        return obj.owner.nickname

    def get_owner_profile_image(self, obj):
        return obj.owner.profile_image.url

    def get_author_profile_image(self, obj):
        return obj.author.profile_image.url

    class Meta:
        model = Painting
        fields = (
            "id",
            "title",
            "content",
            "author",
            "owner",
            "after_image",
            "created_at",
            "updated_at",
            "is_auction",
            "owner_profile_image",
            "author_profile_image",
        )


# 유화 리스트 serializer
class PaintingListSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    owner = serializers.SerializerMethodField()

    def get_author(self, obj):
        return obj.author.nickname

    def get_owner(self, obj):
        return obj.owner.nickname

    class Meta:
        model = Painting
        fields = (
            "id",
            "author",
            "owner",
            "title",
            "content",
            "after_image",
            "created_at",
            "updated_at",
            "style",
            "is_auction",
        )
