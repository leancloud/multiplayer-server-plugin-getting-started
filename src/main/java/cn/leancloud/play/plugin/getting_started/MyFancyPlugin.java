package cn.leancloud.play.plugin.getting_started;

import cn.leancloud.play.plugin.AbstractPlugin;
import cn.leancloud.play.plugin.BoundRoom;
import cn.leancloud.play.plugin.context.*;
import cn.leancloud.play.plugin.request.*;

import java.util.Map;

public class MyFancyPlugin extends AbstractPlugin {
    public MyFancyPlugin(BoundRoom room, Map<String, Object> initConfigs) {
        super(room);
        // do some constructor stuff
    }

    @Override
    public void onCreateRoom(CreateRoomContext ctx) {
        CreateRoomRequest req = ctx.getRequest();

        // do something with req

        // process create room
        ctx.continueProcess();

        // do something after processing create room
    }

    @Override
    public void onBeforeJoinRoom(BeforeJoinRoomContext ctx) {
        JoinRoomRequest req = ctx.getRequest();

        // do something with req

        // process join room
        ctx.continueProcess();

        // do something after processing join room
    }

    @Override
    public void onBeforeLeaveRoom(BeforeLeaveRoomContext ctx) {
        LeaveRoomRequest req = ctx.getRequest();
        // do something with req

        // process leave room
        ctx.continueProcess();

        // do something after processing leave room
    }

    @Override
    public void onBeforeSetRoomProperties(BeforeSetRoomPropertiesContext ctx) {
        SetRoomPropertiesRequest req = ctx.getRequest();

        // do something with req

        // process set room properties
        ctx.continueProcess();

        // do something after processing set room properties
    }

    @Override
    public void onBeforeSetPlayerProperties(BeforeSetPlayerPropertiesContext ctx) {
        SetPlayerPropertiesRequest req = ctx.getRequest();

        // do something with req

        // process set player properties
        ctx.continueProcess();

        // do something after processing set player properties
    }

    @Override
    public void onBeforeSetRoomSystemProperties(BeforeSetRoomSystemPropertiesContext ctx) {
        SetRoomSystemPropertiesRequest req = ctx.getRequest();

        // do something with req

        // process set room system properties
        ctx.continueProcess();

        // do something after processing set room system properties
    }

    @Override
    public void onBeforeSendEvent(BeforeSendEventContext ctx) {
        SendEventRequest req = ctx.getRequest();

        // do something with req

        // process raise rpc
        ctx.continueProcess();

        // do something after processing raise rpc
    }

    @Override
    public void onDestroyRoom(DestroyRoomContext ctx) {
        DestroyRoomRequest req = ctx.getRequest();

        // do something with req

        // process close room
        ctx.continueProcess();

        // do something after processing close room
    }
}
