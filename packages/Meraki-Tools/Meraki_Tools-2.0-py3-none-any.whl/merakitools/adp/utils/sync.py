def merge_sgts(src, sgts, is_base, sync_session, log=None, obj=None):
    changed_objs = []
    try:
        iseservers = ISEServer.objects.all()
        organizations = Organization.objects.filter(dashboard__syncsession=sync_session)
        for s in sgts:
            tag_num = None
            if isinstance(s, dict):
                if "value" in s:
                    tag_num = s["value"]
                elif "tag" in s:
                    tag_num = s["tag"]
            else:
                tag_num = None
            tid = s["id"] if "id" in s else s["groupId"]
            append_log(log, "db_trustsec::merge_sgts::evaluating", tag_num, "(", tid, ")...")

            if tag_num is not None:
                # Look up tag, and see if the source matches the current input. If so, check for updates...
                tagds = TagData.objects.filter(source_id=tid)
                if len(tagds) > 0:
                    tag = tagds[0].tag
                else:
                    tag = None

                if tag:
                    if is_base:
                        append_log(log, "db_trustsec::merge_sgts::sgt::" + src + "::", tag_num,
                                   "exists in database; updating...")
                        tag.tag_number = tag_num
                        if tag.name != s["name"] and tag.cleaned_name() != s["name"]:
                            tag.name = s["name"]
                        tag.description = s["description"].replace("'", "").replace('"', "")
                        tag.save()
                        changed_objs.append(tag)
                    else:
                        append_log(log, "db_trustsec::merge_sgts::sgt::" + src + "::", tag_num,
                                   "exists in database; not base, only add data...")
                    created = False
                else:
                    if src == "meraki":
                        tag, created = Tag.objects.get_or_create(tag_number=tag_num,
                                                                 defaults={"name": s["name"],
                                                                           "description": s["description"],
                                                                           "origin_org": obj,
                                                                           "syncsession": sync_session})
                    else:
                        tag, created = Tag.objects.get_or_create(tag_number=tag_num,
                                                                 defaults={"name": s["name"],
                                                                           "description": s["description"],
                                                                           "origin_ise": obj,
                                                                           "syncsession": sync_session})
                if created:
                    changed_objs.append(tag)
                    append_log(log, "db_trustsec::merge_sgts::creating tag", tag_num, "...")

                # Ensure that all Data objects exist in DB
                if not tag.push_delete:
                    append_log(log, "db_trustsec::merge_sgts::sgt::" + src + "::", tag_num,
                               "writing raw data to database...")
                    if src == "meraki":
                        TagData.objects.update_or_create(tag=tag, organization=obj,
                                                         defaults={"source_id": s["groupId"],
                                                                   "source_data": json.dumps(s),
                                                                   "source_ver": s["versionNum"],
                                                                   "last_sync": make_aware(datetime.datetime.now())})
                        # Ensure TagData objects exist for ISE
                        for i in iseservers:
                            TagData.objects.get_or_create(tag=tag, iseserver=i)
                        # Ensure TagData objects exist for all Meraki Orgs
                        for o in organizations:
                            TagData.objects.get_or_create(tag=tag, organization=o)
                    elif src == "ise":
                        if s.get("generationId"):
                            TagData.objects.update_or_create(tag=tag, iseserver=obj,
                                                             defaults={"source_id": s["id"],
                                                                       "source_data": json.dumps(s),
                                                                       "source_ver": s["generationId"],
                                                                       "last_sync":
                                                                           make_aware(datetime.datetime.now())})
                        else:
                            TagData.objects.update_or_create(tag=tag, iseserver=obj,
                                                             defaults={"source_id": s["id"],
                                                                       "source_data": json.dumps(s),
                                                                       "last_sync":
                                                                           make_aware(datetime.datetime.now())})
                        # Ensure TagData objects exist for all Meraki Orgs
                        for o in organizations:
                            TagData.objects.get_or_create(tag=tag, organization=o)

        return changed_objs
    except Exception as e:    # pragma: no cover
        append_log(log, "db_trustsec::merge_sgts::Exception in merge_sgts: ", e, traceback.format_exc())
    return changed_objs