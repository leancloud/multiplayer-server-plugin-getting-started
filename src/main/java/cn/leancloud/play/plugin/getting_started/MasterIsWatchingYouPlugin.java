package cn.leancloud.play.plugin.getting_started;

import cn.leancloud.play.collection.PlayObject;
import cn.leancloud.play.plugin.AbstractPlugin;
import cn.leancloud.play.plugin.Actor;
import cn.leancloud.play.plugin.BoundRoom;
import cn.leancloud.play.plugin.context.BeforeSendEventContext;
import cn.leancloud.play.plugin.request.ReceiverGroup;
import cn.leancloud.play.plugin.request.SendEventOptions;
import cn.leancloud.play.plugin.request.SendEventRequest;

import java.util.ArrayList;
import java.util.List;


public class MasterIsWatchingYouPlugin extends AbstractPlugin {
    public MasterIsWatchingYouPlugin(BoundRoom room) {
        super(room);
    }

    @Override
    public void onBeforeSendEvent(BeforeSendEventContext ctx) {
        SendEventRequest req = ctx.getRequest();
        BoundRoom room = getBoundRoom();
        Actor master = room.getMaster();
        if (master == null) {
            // no master in this room
            // reject and swallow this request
            ctx.skipProcess();
            return;
        }

        boolean masterIsInTargets = true;
        List<Integer> targetActors = req.getTargetActorIds();
        if (!targetActors.isEmpty() &&
                targetActors.stream().noneMatch(actorId -> actorId == master.getActorId())) {
            masterIsInTargets = false;

            ArrayList<Integer> newTargets = new ArrayList<>(targetActors);
            newTargets.add(master.getActorId());
            req.setTargetActorIds(newTargets);
        }

        ctx.continueProcess();

        if (!masterIsInTargets) {
            String msg = String.format("actor %d is sending sneaky rpc", req.getFromActorId());
            room.sendEventToReceiverGroup(ReceiverGroup.ALL,
                    master.getActorId(),
                    (byte)0,
                    new PlayObject().fluentPut("data", msg),
                    SendEventOptions.emptyOption);
        }
    }
}
