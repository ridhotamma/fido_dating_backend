from django.contrib.auth.models import AbstractUser
from django.db import models

from media_utils import ImageVariantMixin, get_media_storage


class CustomUser(AbstractUser, ImageVariantMixin):
    bio = models.TextField(blank=True, null=True)
    avatar = models.ImageField(
        upload_to="avatars/", blank=True, null=True, storage=get_media_storage()
    )
    avatar_sm = models.URLField(blank=True, null=True)
    avatar_md = models.URLField(blank=True, null=True)
    avatar_lg = models.URLField(blank=True, null=True)
    phone_number = models.CharField(max_length=20, unique=True, null=True, blank=True)
    coins = models.IntegerField(default=0)  # Add coin balance
    last_claimed = models.DateField(null=True, blank=True)  # Track last claim date

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.avatar:
            storage = get_media_storage()
            base_path = f"avatars/{self.pk}/avatar"
            variants = self.generate_variants(self.avatar, storage, base_path)
            self.avatar_sm = variants.get("sm")
            self.avatar_md = variants.get("md")
            self.avatar_lg = variants.get("lg")
            super().save(update_fields=["avatar_sm", "avatar_md", "avatar_lg"])

    def __str__(self):
        return self.username


class Follow(models.Model):
    follower = models.ForeignKey(
        "CustomUser", related_name="following_set", on_delete=models.CASCADE
    )
    following = models.ForeignKey(
        "CustomUser", related_name="followers_set", on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("follower", "following")

    def __str__(self):
        return f"{self.follower.username} follows {self.following.username}"


class CoinClaimHistory(models.Model):
    user = models.ForeignKey(
        CustomUser, related_name="coin_claims", on_delete=models.CASCADE
    )
    claimed_at = models.DateTimeField(auto_now_add=True)
    amount = models.IntegerField(default=10)

    class Meta:
        ordering = ["-claimed_at"]
        verbose_name = "Coin Claim History"
        verbose_name_plural = "Coin Claim Histories"

    def __str__(self):
        return f"{self.user.username} claimed {self.amount} coins at {self.claimed_at}"
