from main import db, User, BodyPart, Exercise

if __name__ == '__main__':
    db.drop_all()
    db.create_all()

    bp1 = BodyPart(name="chest")
    bp2 = BodyPart(name="bicep")
    db.session.add(bp1)
    db.session.add(bp2)

    e1 = Exercise(name="Bicep Curl", description="Contract bicep while holding weight then release")
    e1.uses.append(bp2)
    e2 = Exercise(name="Push up", description="Everyone knows what push up is")
    e2.uses.append(bp1)
    db.session.add(e1)
    db.session.add(e2)

    u1 = User(username="ArnoldSchwazzaneger123")
    u1.targets.append(bp1)

    u2 = User(username="DwanedaRockJohnson")
    u2.targets.extend([bp1, bp2])

    db.session.add_all([u1, u2])


    db.session.commit()
