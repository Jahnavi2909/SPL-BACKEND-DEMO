from django.contrib import admin
from django import forms
from django.core.exceptions import ValidationError

from .models import Match, MatchPlayingXI,PointsTable,PlayerStats
from core.models import Player


# 🔥 FORM (handles filtering + validation)
class MatchPlayingXIForm(forms.ModelForm):
    class Meta:
        model = MatchPlayingXI
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # ✅ When selecting match (POST data)
        if 'match' in self.data:
            try:
                match_id = int(self.data.get('match'))
                match = Match.objects.get(id=match_id)

                # 🔹 Team1 players
                self.fields['team1_players'].queryset = Player.objects.filter(
                    team=match.team1
                )

                # 🔹 Team2 players
                self.fields['team2_players'].queryset = Player.objects.filter(
                    team=match.team2
                )

                # 🔹 Captains
                self.fields['team1_captain'].queryset = Player.objects.filter(
                    team=match.team1
                )

                self.fields['team2_captain'].queryset = Player.objects.filter(
                    team=match.team2
                )

            except:
                pass

        # ✅ When editing existing object
        elif self.instance.pk:
            match = self.instance.match

            self.fields['team1_players'].queryset = Player.objects.filter(
                team=match.team1
            )

            self.fields['team2_players'].queryset = Player.objects.filter(
                team=match.team2
            )

            self.fields['team1_captain'].queryset = Player.objects.filter(
                team=match.team1
            )

            self.fields['team2_captain'].queryset = Player.objects.filter(
                team=match.team2
            )

        else:
            # ❗ Initial load (no match selected)
            self.fields['team1_players'].queryset = Player.objects.none()
            self.fields['team2_players'].queryset = Player.objects.none()
            self.fields['team1_captain'].queryset = Player.objects.none()
            self.fields['team2_captain'].queryset = Player.objects.none()

    # 🔥 VALIDATION (SAFE — no crashes)
    def clean(self):
        cleaned_data = super().clean()

        t1_players = cleaned_data.get('team1_players') or []
        t2_players = cleaned_data.get('team2_players') or []
        t1_captain = cleaned_data.get('team1_captain')
        t2_captain = cleaned_data.get('team2_captain')
        match = cleaned_data.get('match')

        # ❗ If match not selected yet → skip validation
        if not match:
            return cleaned_data

        # 🔥 Exactly 11 players
        if len(t1_players) != 11:
            raise ValidationError("Team1 must have exactly 11 players")

        if len(t2_players) != 11:
            raise ValidationError("Team2 must have exactly 11 players")

        # 🔥 Ensure correct team players
        for p in t1_players:
            if p.team != match.team1:
                raise ValidationError(f"{p} does not belong to Team1")

        for p in t2_players:
            if p.team != match.team2:
                raise ValidationError(f"{p} does not belong to Team2")

        # 🔥 Captain validation
        if t1_captain not in t1_players:
            raise ValidationError("Team1 captain must be in Playing XI")

        if t2_captain not in t2_players:
            raise ValidationError("Team2 captain must be in Playing XI")

        return cleaned_data


# ADMIN CONFIG
@admin.register(MatchPlayingXI)
class MatchPlayingXIAdmin(admin.ModelAdmin):
    form = MatchPlayingXIForm
    filter_horizontal = ('team1_players', 'team2_players')


# Register Match also
admin.site.register(Match)
admin.site.register(PointsTable)


admin.site.register(PlayerStats)
