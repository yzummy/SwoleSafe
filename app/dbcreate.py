from main import db, User, BodyPart, Exercise

if __name__ == '__main__':
    db.drop_all()
    db.create_all()

    bp1 = BodyPart(name="chest")
    bp2 = BodyPart(name="biceps")
    bp3 = BodyPart(name='quadriceps')
    bp4 = BodyPart(name='hamstrings')
    bp5 = BodyPart(name='deltoids')
    bp6 = BodyPart(name='triceps')
    bp7 = BodyPart(name='back')
    bp8 = BodyPart(name='glutes')
    bp9 = BodyPart(name='chest')
    bp10 = BodyPart(name='forearms')
    bp11 = BodyPart(name='abs')

    db.session.add_all([bp1, bp2, bp3, bp4, bp5, bp6, bp7, bp8, bp9, bp10, bp11])

    e1 = Exercise(name="Bicep Curl", description="Contract bicep while holding weight then release slowly")
    e1.uses.append(bp2)

    e2 = Exercise(name="Front Raise", description="Raise dumbells in front of you")
    e2.uses.append(bp5)

    e3 = Exercise(name="Squat", description="Pretend like you are sitting down and getting up from an invisible chair")
    e3.uses.extend([bp3, bp4, bp8])

    e4 = Exercise(name="Pushup", description="Keep your back flat. Remember to breathe.")
    e4.uses.extend([bp1, bp5, bp6, bp11])


    db.session.add_all([e1, e2, e3])

    u1 = User(username="ArnoldSchwazzaneger123", password="abc", level="advanced")
    u1.targets.extend([bp5, bp1, bp7])

    u2 = User(username="DwanedaRockJohnson", password="123", level="beginner")
    u2.targets.extend([bp2, bp3])

    u3 = User(username="Batman", password="a;lkdjflkdsaf", level="intermediate")
    u3.targets.extend([bp1, bp2, bp3, bp4, bp5, bp6, bp7, bp8, bp9, bp10, bp11])

    u4 = User(username="Squatman", password="ilovesquats", level="advanced")
    u4.targets.extend([bp4])

    db.session.add_all([u1, u2, u3, u4])

    db.session.commit()
