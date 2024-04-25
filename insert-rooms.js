db.rooms.insertMany([
  {
    "name": "Gemütliches Cottage",
    "beschreibung": "Ein charmantes Cottage am Seeufer",
    "adresse": "Bergstrasse 28, 3952 Berghausen",
    "besitzer_id": "emma.jackson@example.com",
    "zimmer": 2,
    "fläche": 120
  },
  {
    "name": "Bergidyll",
    "beschreibung": "Ein abgelegenes Berghaus mit Panoramablick",
    "adresse": "Bergstrasse 90, 3952 Berghausen",
    "bewohner_ids": ["emma.jackson@example.com"],
    "besitzer_id": "john.doe@example.com",
    "zimmer": 3,
    "fläche": 180,
    "gebucht_von": ISODate("2024-04-10T00:00:00Z"),
    "gebucht_bis": ISODate("2024-04-15T00:00:00Z")
  },
  {
    "name": "Strandvilla",
    "beschreibung": "Eine luxuriöse Strandvilla mit eigenem Zugang zum Meer",
    "adresse": "Strandstrasse 1b, 9522 Meer",
    "bewohner_ids": ["james.brown@example.com", "sophie.wilson@example.com"],
    "besitzer_id": "michael.adams@example.com",
    "zimmer": 4,
    "fläche": 250,
    "gebucht_von": ISODate("2024-05-01T00:00:00Z"),
    "gebucht_bis": ISODate("2024-05-10T00:00:00Z")
  },
  {
    "name": "Stadtpalast",
    "beschreibung": "Ein prächtiger Palast im Herzen der Stadt",
    "adresse": "Stadtweg 8, 5202 Städtchen",
    "bewohner_ids": ["michael.adams@example.com", "sarah.johnson@example.com"],
    "besitzer_id": "sophie.wilson@example.com",
    "zimmer": 6,
    "fläche": 400,
    "gebucht_von": ISODate("2024-06-15T00:00:00Z"),
    "gebucht_bis": ISODate("2024-06-30T00:00:00Z")
  },
  {
    "name": "Alpenhütte",
    "adresse": "Alpenweg 29, 0392 Rue des Alpes",
    "bewohner_ids": ["sarah.johnson@example.com"],
    "besitzer_id": "james.brown@example.com",
    "zimmer": 2,
    "fläche": 100,
    "gebucht_von": ISODate("2024-07-05T00:00:00Z"),
    "gebucht_bis": ISODate("2024-07-12T00:00:00Z")
  },
  {
    "name": "Seehaus",
    "beschreibung": "Ein modernes Haus direkt am See",
    "adresse": "Am See 2a, 1270 Thun",
    "bewohner_ids": ["john.doe@example.com", "michael.adams@example.com"],
    "besitzer_id": "sarah.johnson@example.com",
    "zimmer": 3,
    "fläche": 180,
    "gebucht_von": ISODate("2024-08-20T00:00:00Z"),
    "gebucht_bis": ISODate("2024-08-25T00:00:00Z")
  },
  {
    "name": "Waldhütte",
    "beschreibung": "Eine gemütliche Hütte mitten im Wald",
    "adresse": "Waldstrasse 66, 3456 Waldhausen",
    "bewohner_ids": ["sophie.wilson@example.com", "john.doe@example.com"],
    "besitzer_id": "james.brown@example.com",
    "zimmer": 2,
    "fläche": 120,
    "gebucht_von": ISODate("2024-09-01T00:00:00Z"),
    "gebucht_bis": ISODate("2024-09-07T00:00:00Z")
  },
  {
    "name": "Ferienwohnung am Fluss",
    "adresse": "Flussstrasse 3, 10115 Berlin",
    "besitzer_id": "john.doe@example.com",
    "zimmer": 1,
    "fläche": 80
  },
  {
    "name": "kleine Wohnung in Nähe der Stadt",
    "adresse": "Stadtstrasse 3, 10115 Berlin",
    "besitzer_id": "james.brown@example.com",
    "zimmer": 1,
    "fläche": 30
  },
  {
    "name": "Haus am Waldrand",
    "adresse": "Waldweg 8, 7612 Waldhausen",
    "besitzer_id": "jane.smith@example.com",
    "zimmer": 4,
    "fläche": 180
  },
  {
    "name": "Chalet am See",
    "beschreibung": "Ein gemütliches Chalet mit Blick auf den See",
    "adresse": "Seestrasse 47, 8002 Zürich",
    "bewohner_ids": ["james.brown@example.com"],
    "besitzer_id": "sophie.wilson@example.com",
    "zimmer": 3,
    "fläche": 150,
    "gebucht_von": ISODate("2024-11-05T00:00:00Z"),
    "gebucht_bis": ISODate("2024-11-15T00:00:00Z")
  },
  {
    "name": "Stadtwohnung",
    "beschreibung": "Eine moderne Wohnung im Stadtzentrum",
    "adresse": "Stadtzentrumstrasse 12, 80331 München",
    "bewohner_ids": ["jane.smith@example.com"],
    "besitzer_id": "emma.jackson@example.com",
    "zimmer": 2,
    "fläche": 100,
    "gebucht_von": ISODate("2024-12-01T00:00:00Z"),
    "gebucht_bis": ISODate("2024-12-10T00:00:00Z")
  },
  {
    "name": "Landhaus",
    "beschreibung": "Ein idyllisches Landhaus mit großem Garten",
    "adresse": "Landhausweg 5, 10407 Berlin",
    "bewohner_ids": ["john.doe@example.com", "james.brown@example.com"],
    "besitzer_id": "sarah.johnson@example.com",
    "zimmer": 4,
    "fläche": 200,
    "gebucht_von": ISODate("2025-01-05T00:00:00Z"),
    "gebucht_bis": ISODate("2025-01-15T00:00:00Z")
  },
  {
    "name": "Ferienhaus am Wald",
    "adresse": "Waldweg 88, 76131 Karlsruhe",
    "besitzer_id": "jane.smith@example.com",
    "zimmer": 3,
    "fläche": 160
  },
  {
    "name": "Strandhaus",
    "beschreibung": "Ein charmantes Strandhaus mit Meerblick",
    "adresse": "Strandweg 101, 59821 Arnsberg",
    "besitzer_id": "sophie.wilson@example.com",
    "zimmer": 2,
    "fläche": 110
  },
  {
    "name": "Hütte im Tal",
    "beschreibung": "Eine einfache Hütte inmitten eines Tals",
    "adresse": "Talweg 33, 8001 Zürich",
    "bewohner_ids": ["sophie.wilson@example.com", "john.doe@example.com"],
    "besitzer_id": "jane.smith@example.com",
    "zimmer": 1,
    "fläche": 70,
    "gebucht_von": ISODate("2025-04-01T00:00:00Z"),
    "gebucht_bis": ISODate("2025-04-10T00:00:00Z")
  },
  {
    "name": "Ferienwohnung am Berg",
    "beschreibung": "Eine gemütliche Ferienwohnung in den Bergen",
    "adresse": "Bergstrasse 111, 6020 Innsbruck",
    "bewohner_ids": ["jane.smith@example.com"],
    "besitzer_id": "james.brown@example.com",
    "zimmer": 2,
    "fläche": 90,
    "gebucht_von": ISODate("2025-05-01T00:00:00Z"),
    "gebucht_bis": ISODate("2025-05-15T00:00:00Z")
  },
  {
    "name": "Seeapartment",
    "beschreibung": "Ein modernes Apartment mit Seeblick",
    "adresse": "Seeblickstrasse 20, 6005 Luzern",
    "bewohner_ids": ["emma.jackson@example.com"],
    "besitzer_id": "michael.adams@example.com",
    "zimmer": 1,
    "fläche": 60,
    "gebucht_von": ISODate("2025-06-01T00:00:00Z"),
    "gebucht_bis": ISODate("2025-06-10T00:00:00Z")
  },
  {
    "name": "Almhütte",
    "adresse": "Almhüttenweg 14, 6100 Seefeld",
    "besitzer_id": "sophie.wilson@example.com",
    "zimmer": 2,
    "fläche": 100
  },
  {
    "name": "Wasserhaus",
    "beschreibung": "Ein modernes Haus auf Stelzen im Wasser",
    "adresse": "Wasserweg 47, 70173 Stuttgart",
    "besitzer_id": "michael.adams@example.com",
    "zimmer": 3,
    "fläche": 200
  },
  {
    "name": "Ferienhaus am Flussufer",
    "beschreibung": "Ein gemütliches Ferienhaus am Ufer eines Flusses",
    "adresse": "Flussuferstrasse 12, 10179 Berlin",
    "bewohner_ids": ["john.doe@example.com"],
    "besitzer_id": "james.brown@example.com",
    "zimmer": 2,
    "fläche": 120,
    "gebucht_von": ISODate("2025-09-01T00:00:00Z"),
    "gebucht_bis": ISODate("2025-09-10T00:00:00Z")
  }
])
